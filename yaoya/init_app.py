# session_stateの初期化

import streamlit as st

class StreamlitSessionManager:
    def __init__(self) -> None:
        self._session_state = st.session_state

    def get_user(self) -> User:
        return self._session_state["user"]

    def set_user(self, user: User) -> None:
        self._session_state["user"] = user

def init_session() -> StreamlitSessionManager:
    mockdir = Path(TemporaryDirectory().name) # (A)
    mockdir.mkdir(exist_ok=True)
    mockdb = MockDB(mockdir.joinpath("mock.db"))
    session_db = MockSessionDB(mockdir.joinpath("session.json"))
    ssm = StreamlitSessionManager()
    return ssm

# ページの初期化
def init_pages(ssm: StreamlitSessionManager) -> list[BasePage]:
    pages = [
        # ページクラスを追加
    ]
    return pages

# アプリケーションの初期化
def init_app(ssm: StreamlitSessionManager, pages: list[BasePage]) -> MultiPageApp:
    app = MultiPageApp(ssm, pages)
    return app