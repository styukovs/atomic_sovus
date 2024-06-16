import os
import uuid
from typing import List, Optional

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from atomic_sovus.chain import RelevantFAQ, RelevantManual, get_relevant_faq, get_relevant_manuals
from atomic_sovus.settings import N_PAGES

st.set_page_config(
    page_title="Поиск инструкций",
    page_icon="👋",
)

st.title("🚀 Поиск по мануалам")


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


if prompt := st.chat_input("Введите вопрос"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    manuals = get_relevant_manuals(prompt)

    st.chat_message("assistant").write(":closed_book: Смотрите что я смог найти")
    st.session_state.messages.append(
        {"role": "assistant", "content": ":closed_book: Смотрите что я смог найти", "manuals": manuals}
    )

    render_manuals(manuals)
