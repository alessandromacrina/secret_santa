import streamlit as st
import random
import smtplib
from email.mime.text import MIMEText

def send_email(sender_email, sender_password, recipient_email, subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = recipient_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        st.error(f"Errore durante l'invio dell'email a {recipient_email}: {e}")

st.title("Babbo Natale Segreto 🎅")

# Input per i partecipanti
st.header("Inserisci i partecipanti")
with st.form("secret_santa_form"):
    participants_input = st.text_area("Inserisci i nomi e le email dei partecipanti, uno per riga (es. Mario Rossi, mario@example.com)")
    sender_email = st.text_input("Inserisci l'email del mittente")
    sender_password = st.text_input("Inserisci la password del mittente", type="password")
    submitted = st.form_submit_button("Esegui estrazione")

if submitted:
    if not participants_input or not sender_email or not sender_password:
        st.error("Tutti i campi sono obbligatori!")
    else:
        # Parsing input dei partecipanti
        participants = []
        for line in participants_input.split("\n"):
            parts = line.split(",")
            if len(parts) == 2:
                name = parts[0].strip()
                email = parts[1].strip()
                participants.append((name, email))
            else:
                st.error("Formato errato: ogni riga deve essere 'Nome, Email'")
                break

        if len(participants) < 2:
            st.error("Devono esserci almeno 2 partecipanti!")
        else:
            # Generazione estrazioni
            names = [p[0] for p in participants]
            emails = [p[1] for p in participants]
            shuffled_names = names[:]
            random.shuffle(shuffled_names)

            while any(name == shuffled_name for name, shuffled_name in zip(names, shuffled_names)):
                random.shuffle(shuffled_names)

            pairs = list(zip(names, shuffled_names))

            # Invio email ai partecipanti
            st.write("Invio email in corso...")
            for giver, receiver in pairs:
                receiver_email = emails[names.index(receiver)]
                subject = "Il tuo Babbo Natale Segreto! 🎅"
                body = f"Ciao {giver},\n\nSei il Babbo Natale Segreto di {receiver}!\n\nBuon divertimento e buone feste! 🎄"
                send_email(sender_email, sender_password, receiver_email, subject, body)

            st.success("Tutte le email sono state inviate con successo!")
