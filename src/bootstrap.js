// Catch module/chunk loading failures before the game starts.
import('./main.js').catch(error => {
  const status = document.getElementById('status');
  status.hidden = false;
  status.textContent = '게임 모듈 로딩 실패: ' + error.message + '\n인터넷 연결을 확인하고 페이지를 새로고침하세요.';
  console.error(error);
});
