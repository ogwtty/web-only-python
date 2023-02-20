# main.py
import streamlit as st
import dataset
db = dataset.connect('sqlite:///:memory:')
from dataclasses import dataclass

class StreamlitSessionManager:
    def __init__(self) -> None:
        self._session_state = st.session_state

    def get_user(self) -> User:
        return self._session_state["user"]

    def set_user(self, user: User) -> None:
        self._session_state["user"] = user

class SessionKey(Enum):
    USER = auto()


class StreamlitSessionManager:
    def get_user(self) -> User:
        return self._session_state[SessionKey.USER.name]

    def set_user(self, user: User) -> None:
        self._session_state[SessionKey.USER.name] = user

class MockDB:
    def __init__(self, dbpath: Path) -> None:
        s_dbpath = str(dbpath)
        self._dbname = f"sqlite:///{s_dbpath}"
        self._init_mock_db() # 今後の章で実装

    @contextmanager
    def connect(self) -> Generator[dataset.Database, None, None]:
        db = dataset.connect(self._dbname)
        db.begin()
        try:
            yield db
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

dbpath = Path("sample.db")
mock_db = MockDB(dbpath)

# With句でテーブルの定義&データの追加
with mock_db.connect() as db:
    table: dataset.Table = db["samples"]
    print(table.find_one(id="001"))

class MockSessionDB:
    def __init__(self, dbpath: Path) -> None:
        self._db = TinyDB(dbpath)

    @contextmanager
    def connect(self) -> Generator[TinyDB, None, None]:
        try:
            yield self._db
        except Exception as e:
            raise e

dbpath = Path("sample.json")
mock_session_db = MockSessionDB(dbpath)

with mock_session_db.connect() as db:
    query = Query()
    print(db.search(query.session_id == session_id))
    
class BaseDataModel(Protocol):
    def to_dict(self) -> dict[str, str]:
        pass

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> BaseDataModel:
        pass

class BasePage:
    def __init__(self, page_id: PageId, title: str, ssm: StreamlitSessionManager) -> None:
        self.page_id = page_id.name
        self.title = title
        self.ssm = ssm

    def render(self) -> None:
        pass

class MultiPageApp:
    def __init__(self, ssm: StreamlitSessionManager, pages: list[BasePage], nav_label: str = "ページ一覧") -> None:
        self.pages = {page.page_id: page for page in pages}
        self.ssm = ssm
        self.nav_label = nav_label

    def render(self) -> None:
        # ページ選択ボックスを追加
        page_id = st.sidebar.selectbox(
            self.nav_label, # 選択ボックスのラベル
            list(self.pages.keys()), # ページ一覧
            format_func=lambda page_id: self.pages[page_id].title,
            key=SessionKey.PAGE_ID.name, # (B)
        )

        # ページ描画
        try:
            self.pages[page_id].render() # (A)
        except YaoyaError as e:
            st.error(e)

class PageId(Enum):
    PAGE_ID = auto()



if not st.session_state.get("is_started", False): # 初期化しているかの確認
    ssm = init_session() # session_stateの初期化
    pages = init_pages(ssm) # ページの初期化
    app = init_app(ssm, pages) # アプリケーションの初期化
    st.session_state["is_started"] = True
    st.session_state["app"] = app
    st.set_page_config(page_title="八百屋さんEC", layout="wide") # Streamlitのページ設定

app = st.session_state.get("app", None)
if app is not None:
    app.render()