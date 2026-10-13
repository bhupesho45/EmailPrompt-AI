
import streamlit as st

from email_service import generate_email_reply

st.set_page_config(
    page_title="EmailPrompt AI",
    page_icon="📧",
    layout="centered",
)

st.title("📧 EmailPrompt AI")
st.caption("AI-Powered Email Reply Assistant")

st.write(
    "Paste an email, choose your preferred tone, "
    "and generate a reply using AI."
)

# User input
email = st.text_area(
    "Original email",
    placeholder="Paste the email you received here...",
    height=220,
)

tone = st.selectbox(
    "Choose reply tone",
    ["Professional", "Friendly", "Formal", "Short"],
)

# Generate reply
if st.button("Generate Reply", type="primary"):
    if not email.strip():
        st.warning("Please paste an email first.")

    else:
        with st.spinner("Generating your reply..."):
            try:
                reply = generate_email_reply(
                    email=email,
                    tone=tone,
                )

                st.session_state["generated_reply"] = reply
                st.session_state["last_tone"] = tone

            except Exception as error:
                st.error(
                    "Could not generate the reply. "
                    "Check your API key, model availability, "
                    "internet connection, and Groq account limits."
                )
                # Useful during local development.
                st.exception(error)

# Display the generated reply
if st.session_state.get("generated_reply"):
    st.divider()
    st.subheader("Generated Reply")

    st.caption(
        f"Selected tone: {st.session_state['last_tone']}"
    )

    edited_reply = st.text_area(
        "Review and edit your reply",
        value=st.session_state["generated_reply"],
        height=220,
        key="editable_reply",
    )

    if st.button("Update Draft"):
        st.session_state["generated_reply"] = edited_reply
        st.success("Draft updated.")

    st.download_button(
        label="Download Reply",
        data=edited_reply,
        file_name="email_reply.txt",
        mime="text/plain",
    )

    st.caption(
        "Review the draft before sending it from your email client."
    )
