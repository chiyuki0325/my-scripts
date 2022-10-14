from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import subprocess as sp

app = FastAPI()


@app.get('/')
async def get_info():
    process = sp.Popen('xdotool getwindowname $(xdotool search --name SFMB)', shell=True, stdout=sp.PIPE)
    process.wait()
    window_name = process.stdout.read().decode().replace('\n', '')
    if 'Playing' in window_name:
        return {'status': 'playing', 'level_name': window_name.split(' Playing \'')[1].split('\' by ')[0],
                'author': window_name.split('\' by ')[1]}
    else:
        return {'status': 'not_playing'}
    
    
@app.get('/frontend')
async def frontend():
    return HTMLResponse(open('mm_frontend.html').read())


uvicorn.run(app=app, host='localhost', port=8889)
