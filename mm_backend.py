from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import subprocess as sp

app = FastAPI()

level_name_cache: str = ''
clears: int = 0
is_challenge: bool = True

@app.get('/status')
async def get_info():
    process = sp.Popen('xdotool getwindowname $(xdotool search --name SFMB)', shell=True, stdout=sp.PIPE)
    process.wait()
    window_name: str = process.stdout.read().decode().replace('\n', '')
    if 'Playing' in window_name:
        level_name: str = window_name.split(' Playing \'')[1].split('\' by ')[0]
        author: str = window_name.split('\' by ')[1]
        if is_challenge:
            global level_name_cache, clears
            if level_name_cache == '':
                level_name_cache = level_name
            if level_name_cache != level_name:
                clears+=1
                level_name_cache = level_name
            return {'status': 'playing', 'level_name': level_name, 'author': author, 'clears': clears, 'is_challenge': True}
        else:
            return {'status': 'playing', 'level_name': level_name, 'author': author, 'is_challenge': False}
    else:
        return {'status': 'not_playing'}

@app.get('/reset')
async def reset():
    global clears
    clears = 0
    return {'status': 'success'}
    
@app.get('/challenge')
async def challenge():
    global is_challenge, level_name_cache
    is_challenge = not is_challenge
    level_name_cache = ''
    return {'status': is_challenge}
    
@app.get('/frontend')
async def frontend():
    return HTMLResponse(open('mm_frontend.html').read())


uvicorn.run(app=app, host='localhost', port=8889)
