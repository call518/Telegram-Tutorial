# Telegram-Tutorial

Python으로 Telegram 메시지를 송수신하는 예제 코드입니다.

## 파일 구성

| 파일 | 설명 |
|------|------|
| `telegram-sender.py` | 메시지 단방향 전송 예제 |
| `telegram-sender-receiver.py` | 메시지 송수신 + 핸들러 등록 예제 |

---

## 사전 준비

코드를 실행하기 전에 **Telegram 봇 생성**과 **채팅방 ID 확인**이 필요합니다.

### 1단계: 봇 생성 및 토큰 발급

1. Telegram에서 **[@BotFather](https://t.me/BotFather)** 를 검색하여 대화를 시작합니다.
2. `/newbot` 명령을 입력합니다.
3. 봇의 **이름(Name)** 을 입력합니다. (예: `My Alert Bot`)
4. 봇의 **사용자명(Username)** 을 입력합니다. 반드시 `Bot` 또는 `bot`으로 끝나야 합니다. (예: `myalert_bot`)
5. 생성 완료 후 BotFather가 **HTTP API 토큰**을 발급해 줍니다.
   ```
   Use this token to access the HTTP API:
   1234567890:ABCdefGHIjklMNOpqrSTUvwxYZ
   ```
   이 값이 `TELEGRAM_TOKEN`입니다. 외부에 노출되지 않도록 주의하세요.

---

### 2단계: 채팅 ID 확인

채팅 ID는 봇이 메시지를 보낼 대상(채팅방)을 식별하는 숫자입니다.  
**1:1 개인 채팅**과 **그룹 채팅** ID를 확인하는 방법이 다릅니다.

#### 공통 준비: getUpdates API 활용

채팅 ID는 Telegram의 `getUpdates` API로 확인합니다.  
먼저 확인하려는 채팅방에서 봇에게 메시지를 보낸 뒤, 브라우저에서 아래 URL에 접속합니다.

```
https://api.telegram.org/bot<TELEGRAM_TOKEN>/getUpdates
```

> `<TELEGRAM_TOKEN>` 부분을 실제 토큰으로 교체하세요.

응답 JSON에서 `chat` → `id` 값을 찾습니다.

```json
{
  "message": {
    "chat": {
      "id": 123456789,
      "type": "private"
    }
  }
}
```

---

#### 1:1 개인 채팅 ID 확인

1. Telegram에서 생성한 봇을 검색해 대화를 시작합니다.
2. 봇에게 아무 메시지나 전송합니다. (예: `hello`)
3. 브라우저에서 `getUpdates` API에 접속합니다.
4. 응답 JSON에서 `"type": "private"` 인 항목의 `chat.id` 값이 **1:1 채팅 ID**입니다.
   - 양수 값입니다. (예: `123456789`)

---

#### 그룹 채팅 ID 확인

그룹 채팅의 경우, 봇이 그룹에 참여해야 메시지를 주고받을 수 있습니다.

1. Telegram에서 그룹 채팅방을 생성하거나 기존 그룹으로 이동합니다.
2. 그룹 멤버 추가에서 생성한 봇을 초대합니다.
3. 그룹 채팅방에서 아무 메시지나 전송합니다.
4. 브라우저에서 `getUpdates` API에 접속합니다.
5. 응답 JSON에서 `"type": "group"` 또는 `"type": "supergroup"` 인 항목의 `chat.id` 값이 **그룹 채팅 ID**입니다.
   - 음수 값입니다. (예: `-1001234567890`)

> **그룹에서 봇이 응답하지 않는 경우:**  
> 그룹 설정 → Privacy Mode가 활성화되어 있으면 봇이 메시지를 수신하지 못합니다.  
> BotFather에서 해당 봇을 선택하고 `/setprivacy` → `Disable`로 변경하세요.

---

### 3단계: 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 입력합니다.

```env
TELEGRAM_TOKEN=여기에_봇_토큰_입력
TELEGRAM_CHAT_ID=여기에_채팅_ID_입력
```

`.env` 파일은 `.gitignore`에 등록되어 있으며, 절대 git에 커밋하지 마세요.

---

## 실행 방법

```bash
# 단방향 메시지 전송
uv run telegram-sender.py

# 메시지 송수신 (polling 방식, Ctrl+C로 종료)
uv run telegram-sender-receiver.py
```

---

## 참고 자료

- [Python으로 Telegram 봇 만들고 메시지 전송하기](https://velog.io/@kylie_03/Python-Telegram-bot-%EB%A7%8C%EB%93%A4%EA%B3%A0-%EB%A9%94%EC%84%B8%EC%A7%80-%EC%A0%84%EC%86%A1%ED%95%98%EA%B8%B0)
- [python-telegram-bot 공식 문서](https://python-telegram-bot.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
