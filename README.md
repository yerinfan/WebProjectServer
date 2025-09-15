
---

## 📌 Server Repository (Backend)

```markdown
# ⚙️ 비동기 통신 웹 프로젝트 - Server

이 레포지토리는 **비동기 채팅/메모 웹 애플리케이션의 서버(Spring Boot 기반)** 부분을 담당합니다.  
WebSocket, Ajax API, Spring Security 등을 통해 백엔드를 구현했습니다.

---

## 🚀 프로젝트 개요
- **목표**: 안정적인 서버 아키텍처와 REST API 기반의 비동기 통신 지원
- **특징**:
  - Spring Boot 기반 REST API
  - WebSocket을 활용한 실시간 채팅 서버
  - Spring Security 기반 권한 관리
  - Oracle DB 연동 (회원/채팅/메모 데이터 관리)

---

## 🛠️ 기술 스택
- **Language**: Java 17
- **Framework**: Spring Boot, Spring MVC, Spring Security
- **DB**: OracleDB, MyBatis
- **Real-time**: WebSocket (SockJS, STOMP)
- **Build Tool**: Maven/Gradle

---

## 🏗️ 시스템 아키텍처

```mermaid
flowchart LR
    subgraph Client[🌐 Web Client]
        UI[HTML/CSS/JS + Thymeleaf]
    end

    subgraph Server[⚙️ Spring Boot Server]
        Controller[Spring MVC Controller]
        Service[Service Layer]
        Repo[MyBatis Repository]
        Security[Spring Security]
        WebSocket[WebSocket (SockJS+STOMP)]
        RESTAPI[REST API (Ajax)]
    end

    subgraph DB[🗄️ Oracle DB]
        UserTable[(Users)]
        ChatTable[(Chats)]
        MemoTable[(Memos)]
    end

    subgraph FaceServer[🤖 Flask Face Recognition]
        FaceAPI[Face Recognition API]
    end

    UI --> |HTTP / Ajax| Controller
    UI <-->|WebSocket| WebSocket
    Controller --> Service --> Repo --> DB
    Security --> Controller
    Service <-->|REST API| FaceServer

---

## 📂 주요 기능
- 회원 관리 (회원가입/로그인/권한 분리)
- 채팅방 생성/참여/메시지 브로드캐스트
- 메모 저장/수정/삭제 (Ajax API)
- 관리자 페이지에서 사용자/메모 관리
- 얼굴 인식 로그인(Flask 서버와 연동 가능)

---

## ⚙️ 실행 방법
1. Oracle DB 실행 후 `application.properties` 설정
2. 서버 실행
   ```bash
   ./mvnw spring-boot:run




