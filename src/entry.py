from urllib.parse import urlsplit

from workers import Response, WorkerEntrypoint

from routes import generator_for_path


class Default(WorkerEntrypoint):
    async def fetch(self, request):
        method = request.method.upper()
        headers = {
            "Cache-Control": "no-store",
            "Content-Type": "text/plain; charset=utf-8",
        }
        generator = generator_for_path(urlsplit(request.url).path)

        if generator is None:
            return Response("Not Found\n", status=404, headers=headers)

        if method == "GET":
            return Response(f"{generator()}\n", headers=headers)
        if method == "HEAD":
            return Response(None, headers=headers)

        headers["Allow"] = "GET, HEAD"
        return Response("Method Not Allowed\n", status=405, headers=headers)
