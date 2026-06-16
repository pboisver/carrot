import sys

from fastapi import Depends, FastAPI, Request

from config_example.shared import get_shared_state

app = FastAPI()

foo = None
bar = None


@app.on_event("startup")
async def startup_event():
    state = get_shared_state()
    global foo, bar
    foo = f"Hello {state['max_value']}"
    bar = "World"
    print(f"Startup event: {sys.argv}")


@app.get("/web")
async def web(request: Request, state: dict = Depends(get_shared_state)):
    return {
        "client_host": request.client.host if request.client else None,
        "max": state["max_value"],
        "render": state["render_value"],
        "foo": foo,
        "bar": bar,
    }
