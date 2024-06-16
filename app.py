import os
import uuid
from typing import List, Optional

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from atomic_sovus.chain import RelevantFAQ, RelevantManual, get_relevant_faq, get_relevant_manuals
from atomic_sovus.settings import N_PAGES

st.title("🚀 Я чат-бот и знаю все об «1С:Предприятие»")
st.caption("💬 Чат-бот технической поддержки")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": ":wave: Здравствуйте, чем могу помочь?"}]
if "state" not in st.session_state:
    st.session_state.state = 1
if "input_disabled" not in st.session_state:
    st.session_state.input_disabled = False


def increment_state() -> None:
    if st.session_state.state == 1:
        enable_input()
    st.session_state.state += 1


def start_again(input_: Optional[str] = None) -> None:
    st.session_state.state = 1
    enable_input()
    st.session_state.messages.append({"role": "assistant", "content": "Чем я еще могу Вам помочь :relieved:?"})
    st.toast(input_)


def disable_input() -> None:
    st.session_state.input_disabled = True


def enable_input() -> None:
    st.session_state.input_disabled = False


def render_manuals(manuals: List[RelevantManual], with_pdf: bool = True) -> None:
    for manual in manuals:
        popover_title = manual.titlename
        with st.popover(popover_title, use_container_width=True):
            if with_pdf:
                filename = manual.filename
                filepath = os.path.join("data/pdf/", filename)
                pdf_viewer(
                    filepath,
                    height=400,
                    pages_to_render=list(range(manual.page, manual.page + N_PAGES)),
                    key=str(uuid.uuid4()),
                )


def render_faqs(faqs: List[RelevantFAQ]) -> None:
    for faq in faqs:
        with st.expander(faq.question):
            st.write(faq.answer)


def render_chat_history() -> None:
    for msg in st.session_state.messages:
        if "manuals" in msg:
            st.chat_message(msg["role"]).write(msg["content"])
            render_manuals(msg["manuals"], with_pdf=False)
        elif "faqs" in msg:
            st.chat_message(msg["role"]).write(msg["content"])
            render_faqs(msg["faqs"])
        else:
            st.chat_message(msg["role"]).write(msg["content"])


def clear_chat_history() -> None:
    del st.session_state.messages


render_chat_history()

if st.session_state.state == 1:
    if prompt := st.chat_input("Введите вопрос", disabled=st.session_state.input_disabled, on_submit=disable_input):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        manuals = get_relevant_manuals(prompt)

        st.chat_message("assistant").write(":closed_book: Смотрите что я смог найти")
        st.session_state.messages.append(
            {"role": "assistant", "content": ":closed_book: Смотрите что я смог найти", "manuals": manuals}
        )

        render_manuals(manuals)

        st.chat_message("assistant").write("Я смог Вам помочь? :wink:")
        st.session_state.messages.append({"role": "assistant", "content": "Я смог Вам помочь? :wink:"})
        st.button("Да, спасибо!", on_click=start_again, kwargs={"input_": "Спасибо за обращение :wink:"})
        st.button("Нет", on_click=increment_state)

if st.session_state.state == 2:
    st.chat_message("assistant").write(
        "Не могу разобраться... :disappointed:\nУточните, пожалуйста, вопрос чтобы я попытался еще раз"
    )
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Не могу разобраться... :disappointed:\nУточните, пожалуйста, вопрос чтобы я попытался еще раз",
        }
    )
    if prompt := st.chat_input("Введите вопрос", disabled=st.session_state.input_disabled, on_submit=disable_input):
        st.chat_message("user").write(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})
        manuals = get_relevant_manuals(prompt)

        st.chat_message("assistant").write(":closed_book: Смотрите что я еще смог найти!")
        st.session_state.messages.append(
            {"role": "assistant", "content": ":closed_book: Смотрите что я еще смог найти!", "manuals": manuals}
        )

        render_manuals(manuals)

        st.chat_message("assistant").write("Я смог Вам помочь? :wink:")
        st.session_state.messages.append({"role": "assistant", "content": "Я смог Вам помочь? :wink:"})
        st.button("Да, спасибо!", on_click=start_again, kwargs={"input_": "Спасибо за обращение :wink:"})
        st.button("Нет", on_click=increment_state)

if st.session_state.state == 3:
    last_prompt = [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"][-1]
    faqs = get_relevant_faq(last_prompt)
    st.chat_message("assistant").write("Смотрите, какие похожие вопросы задавали Ваши коллеги :clipboard:")
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Смотрите, какие похожие вопросы задавали Ваши коллеги :clipboard:",
            "faqs": faqs,
        }
    )
    render_faqs(faqs)
    st.chat_message("assistant").write("Я смог Вам помочь? :wink:")
    st.session_state.messages.append({"role": "assistant", "content": "Я смог Вам помочь? :wink:"})
    st.button("Да, спасибо!", on_click=start_again, kwargs={"input_": "Спасибо за обращение :wink:"})
    st.button("Создать обращение", on_click=increment_state)

if st.session_state.state == 4:
    with st.form(key=str(uuid.uuid4())):
        ticket_type = st.selectbox(
            "Тип обращения",
            (
                "Изменение",
                "Документы по бу и ну",
                "Задание",
                "Запрос",
                "Запрос на изменение",
                "Запрос на обслуживание",
                "Информационный запрос",
                "Инцидент",
                "Комплексный запрос",
                "Претензия",
                "Регламентная работа",
            ),
            index=None,
            placeholder="Выберите тип обращения",
        )

        ticket_name = st.text_input("Наименование обращения")
        ticket_text = st.text_input("Текст обращения")
        st.form_submit_button("Отправить", on_click=start_again, kwargs={"input_": "Заявка отправлена"})
