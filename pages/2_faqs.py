import os
import uuid
from typing import List, Optional

import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

from atomic_sovus.chain import RelevantFAQ, RelevantManual, get_relevant_faq, get_relevant_manuals
from atomic_sovus.settings import N_PAGES

st.set_page_config(
    page_title="Поиск по истории обращений",
    page_icon="👋",
)

st.title("🚀 Поиск по истории обращения")


def render_faqs(faqs: List[RelevantFAQ]) -> None:
    for faq in faqs:
        with st.expander(faq.question):
            st.write(faq.answer)


if prompt := st.chat_input("Введите вопрос"):
    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    manuals = get_relevant_faq(prompt)

    st.chat_message("assistant").write(":closed_book: Смотрите что я смог найти")
    st.session_state.messages.append(
        {"role": "assistant", "content": ":closed_book: Смотрите что я смог найти", "manuals": manuals}
    )

    render_faqs(manuals)
