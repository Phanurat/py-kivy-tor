import asyncio
from aiohttp_socks import open_connection

async def handle_client(reader, writer):
    try:
        request = await reader.read(4096)
        header_line = request.decode(errors='ignore').split('\n')[0]
        method, url, _ = header_line.split()

        if method.upper() == 'CONNECT':
            # ดึง host:port จาก CONNECT
            target_host, target_port = url.split(':')
            target_port = int(target_port)
            print(f"📥 CONNECT {target_host}:{target_port}")

            # เชื่อมต่อผ่าน TOR
            remote_reader, remote_writer = await open_connection(
                proxy_type='socks5',
                proxy_host='127.0.0.1',
                proxy_port=9150,
                host=target_host,
                port=target_port,
                rdns=True  # ✅ DNS ผ่าน TOR
            )

            # ตอบกลับว่า CONNECT สำเร็จ
            writer.write(b"HTTP/1.1 200 Connection established\r\n\r\n")
            await writer.drain()

            async def relay(src, dst):
                try:
                    while True:
                        data = await src.read(4096)
                        if not data:
                            break
                        dst.write(data)
                        await dst.drain()
                except:
                    pass
                finally:
                    dst.close()

            await asyncio.gather(
                relay(reader, remote_writer),
                relay(remote_reader, writer)
            )
        else:
            writer.write(b"HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            await writer.drain()
            writer.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        writer.close()

async def start_proxy():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 62881)
    print("✅ Proxy พร้อมให้บริการที่พอร์ต 62881")
    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(start_proxy())
