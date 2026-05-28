import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Streamlit 불과 얼음의 춤", page_icon="🔮", layout="centered")

st.title("🔮 스트림릿 불과 얼음의 춤 (A Dance of Fire and Ice) 클론")
st.markdown("""
**게임 방법:**
* 두 행성이 서로를 중심으로 회전합니다.
* 파란색 타일과 붉은색 행성이 겹치는 타이밍, 혹은 정확히 수평/수직이 되는 타이밍에 **[스페이스바]**를 누르세요!
* 타이밍이 맞으면 다음 타일로 전진하며, 틀리면 점수가 초기화됩니다.
""")

# HTML5 Canvas와 JavaScript를 이용한 실시간 게임 엔진 주입
game_html = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0;
            overflow: hidden;
        }
        canvas {
            background: #2a2a2a;
            border: 4px solid #444;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.5);
        }
        #scoreBoard {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }
        #message {
            font-size: 18px;
            height: 25px;
            color: #ff4b4b;
            margin-top: 5px;
        }
    </style>
</head>
<body>

    <div id="scoreBoard">Score: <span id="score">0</span></div>
    <canvas id="gameCanvas" width="600" height="300"></canvas>
    <div id="message" id="msg"></div>

    <script>
        const canvas = document.getElementById("gameCanvas");
        const ctx = canvas.getContext("2d");
        const scoreEl = document.getElementById("score");
        const msgEl = document.getElementById("message");

        // 게임 상태 변수
        let score = 0;
        let tiles = [];
        let currentTileIndex = 0;
        
        // 행성 변수 (0: 불/빨강, 1: 얼음/파랑)
        let centerPlanet = 0; 
        let angle = 0;
        const speed = 0.04; // 회전 속도
        const radius = 40;  // 회전 반지름

        // 맵 생성 (일직선 타일 배치)
        const startX = 80;
        const startY = 150;
        const tileSize = 60;
        
        for (let i = 0; i < 20; i++) {
            tiles.push({ x: startX + i * tileSize, y: startY });
        }

        // 키 입력 이벤트 리스너 (스페이스바 포커스 방지 포함)
        window.addEventListener("keydown", function(e) {
            if (e.code === "Space") {
                e.preventDefault(); // 스트림릿 스크롤 방지
                checkTiming();
            }
        });

        function checkTiming() {
            // 얼불춤 메커니즘: 현재 진행 방향(오른쪽) 기준 타일에 도달했을 때의 각도 체크
            // 일직선 맵에서는 정확히 각도가 0도(또는 360도), 파이(180도)에 가까울 때 눌러야 함
            let targetAngle = centerPlanet === 0 ? 0 : Math.PI;
            let normalizedAngle = angle % (Math.PI * 2);
            if (normalizedAngle < 0) normalizedAngle += Math.PI * 2;

            // 판정 범위 (약 0.3 라디안 이내면 성공)
            let diff = Math.abs(normalizedAngle - targetAngle);
            if (diff > Math.PI) diff = Math.PI * 2 - diff;

            if (diff < 0.35) {
                // 성공: 축을 바꾸고 다음 타일로 이동
                score++;
                scoreEl.innerText = score;
                msgEl.style.color = "#00ffcc";
                msgEl.innerText = "Perfect!";
                
                // 중심 축 전환 및 다음 타일 지정
                currentTileIndex = (currentTileIndex + 1) % tiles.length;
                centerPlanet = centerPlanet === 0 ? 1 : 0;
                
                // 각도 보정 (정확한 각도에서 출발하도록 세팅)
                angle = targetAngle; 
            } else {
                // 실패: 점수 초기화
                score = 0;
                scoreEl.innerText = score;
                currentTileIndex = 0;
                centerPlanet = 0;
                angle = 0;
                msgEl.style.color = "#ff4b4b";
                msgEl.innerText = "Overload! (Miss)";
            }
        }

        // 메인 게임 루프
        function update() {
            // 회전 진행
            angle += speed;

            // 그리기 초기화
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // 카메라 연동 (현재 타일이 항상 화면 중앙 부근에 오도록 맵 시프트)
            let offsetX = canvas.width / 2 - tiles[currentTileIndex].x;

            // 1. 타일 그리기
            for (let i = 0; i < tiles.length; i++) {
                ctx.fillStyle = (i === currentTileIndex) ? "#555" : "#333";
                ctx.strokeStyle = (i === currentTileIndex) ? "#00ffcc" : "#555";
                ctx.lineWidth = 2;
                ctx.fillRect(tiles[i].x - 20 + offsetX, tiles[i].y - 20, 40, 40);
                ctx.strokeRect(tiles[i].x - 20 + offsetX, tiles[i].y - 20, 40, 40);
            }

            // 2. 행성 위치 계산
            let currentCenter = tiles[currentTileIndex];
            
            let fireX, fireY, iceX, iceY;

            if (centerPlanet === 0) { // 불(빨강)이 중심축인 경우
                fireX = currentCenter.x;
                fireY = currentCenter.y;
                iceX = fireX + Math.cos(angle) * radius;
                iceY = fireY + Math.sin(angle) * radius;
            } else { // 얼음(파랑)이 중심축인 경우
                iceX = currentCenter.x;
                iceY = currentCenter.y;
                fireX = iceX + Math.cos(angle + Math.PI) * radius; // 반대편에 위치
                fireY = iceY + Math.sin(angle + Math.PI) * radius;
            }

            // 3. 행성 궤도 그리기 (선)
            ctx.beginPath();
            ctx.strokeStyle = "rgba(255,255,255,0.1)";
            ctx.arc(currentCenter.x + offsetX, currentCenter.y, radius, 0, Math.PI * 2);
            ctx.stroke();

            // 4. 행성 실제로 그리기
            // 불 (빨간색)
            ctx.beginPath();
            ctx.fillStyle = "#ff4b4b";
            ctx.shadowColor = "#ff4b4b";
            ctx.shadowBlur = 10;
            ctx.arc(fireX + offsetX, fireY, 10, 0, Math.PI * 2);
            ctx.fill();
            
            // 얼음 (파란색)
            ctx.beginPath();
            ctx.fillStyle = "#00bcff";
            ctx.shadowColor = "#00bcff";
            ctx.shadowBlur = 10;
            ctx.arc(iceX + offsetX, iceY, 10, 0, Math.PI * 2);
            ctx.fill();

            // 그림자 초기화
            ctx.shadowBlur = 0;

            requestAnimationFrame(update);
        }

        // 게임 시작
        update();
    </script>
</body>
</html>
"""

# 스트림릿에 HTML 컴포넌트 렌더링 (높이 및 너비 지정)
# 수정 코드 (scrolling으로 변경)
components.html(game_html, height=400, scrolling=False)

st.info("💡 위 화면을 한번 클릭한 뒤 [스페이스바]를 누르면 게임이 시작됩니다!")
