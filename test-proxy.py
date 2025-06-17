import asyncio

async def handle_client(reader, writer):
    request = await reader.read(4096)
    try:
        header = request.decode().split('\n')[0]
        method, url, _ = header.split()
        print(f"📥 {method} {url}")
        
        # แยก host & port
        if url.startswith("http://"):
            url = url[7:]
        host = url.split('/')[0]
        path = '/' + '/'.join(url.split('/')[1:])
        port = 80

        # เชื่อมต่อ host ปลายทาง
        remote_reader, remote_writer = await asyncio.open_connection(host, port)
        
        # แก้ request line
        modified = request.replace(f"{method} http://{host}{path}".encode(), f"{method} {path}".encode())
        remote_writer.write(modified)
        await remote_writer.drain()

        while True:
            data = await remote_reader.read(4096)
            if not data:
                break
            writer.write(data)
            await writer.drain()
    except Exception as e:
        print("❌ Error:", e)
    finally:
        writer.close()

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8888)
    print("✅ Proxy พร้อมให้บริการที่พอร์ต 8888")
    async with server:
        await server.serve_forever()

asyncio.run(main())
