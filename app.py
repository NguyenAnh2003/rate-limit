from fastapi import FastAPI, Response, Cookie, Depends, Request
from uuid import uuid4
from pydantic import BaseModel

app = FastAPI()

# session storage basic
sessions = {}


# base model
class WordRequest(BaseModel):
    word_id: str
    word: str


def get_session(session_id: str = Cookie(None)):

    if session_id and session_id in sessions:
        return session_id
    else:
        session_id = str(uuid4())  # gen id
        word_id = None
        count = -1
        sessions[session_id] = {"word_id": word_id, "count": count}
        return sessions, session_id  # return _, sessionId


@app.get("/")
def index(request: Request, response: Response):
    try:
        session_id = request.cookies.get("session_id")
        if session_id is None:
            _, session_id = get_session()
            response.set_cookie(key="session_id", value=session_id, httponly=True)
        return {"message": "hello"}

    except Exception as e:
        raise ValueError(e)


@app.post("/create")
def create_gen(request: Request, response: Response, body: WordRequest):
    try:
        session_id = request.cookies.get("session_id")
        word_id, word = body.word_id, body.word  # get word metadata

        user_data = sessions.get(session_id)
        print(f"session: {sessions} data: {user_data}")

        if (
            user_data["word_id"] is None
            or user_data["word_id"] == word_id
            and user_data["count"] < 3
        ):
            user_data["word_id"] = word_id
            user_data["count"] = user_data["count"] + 1
        if user_data["word_id"] == word_id and user_data["count"] == 3:
            user_data["word_id"] = None
            user_data["count"] = -1
            return {"message": "request exceeded"}

        else:
            return {
                "message": f"created with sessionId: {session_id} with word: {word_id} word: {word}"
            }

    except Exception as e:
        raise ValueError(e)
