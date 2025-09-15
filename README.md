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
- **Build Tool**: Maven / Gradle

---

## 🏗️ 시스템 아키텍처

![System Architecture](docs/architecture.png)

- **Spring Boot Server**: REST API, WebSocket, Spring Security 인증/인가 담당  
- **Oracle DB**: 사용자, 채팅, 메모 데이터 관리  
- **Flask Face Recognition Server**: 얼굴 로그인 API 제공  

---

## 📂 주요 기능
- 회원 관리 (회원가입/로그인/권한 분리)
- 채팅방 생성/참여/메시지 브로드캐스트
- 메모 저장/수정/삭제 (Ajax API)
- 관리자 페이지에서 사용자/메모 관리
- 얼굴 인식 로그인(Flask 서버와 연동)

---

## ⚙️ 실행 방법
1. Oracle DB 실행 후 `application.properties` 설정
   ```properties
   spring.datasource.url=jdbc:oracle:thin:@localhost:1521:xe
   spring.datasource.username=your_username
   spring.datasource.password=your_password
   spring.datasource.driver-class-name=oracle.jdbc.OracleDriver
