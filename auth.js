// 공통 인증 처리: 모든 페이지에서 로그인 상태 감지 + 로그아웃 핸들러.
// 사용: <script src="https://cdn.../@supabase/supabase-js@2.45.0/.../supabase.min.js">
//      <script src="config.js">
//      <script src="auth.js">
(function () {
  if (!window.supabase || !window.SUPABASE_URL) {
    console.warn('auth.js: SDK 또는 config 미로드');
    return;
  }

  window.sb = window.supabase.createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY, {
    auth: {
      persistSession: true,
      autoRefreshToken: true,
      storage: window.localStorage,
    },
  });

  function applyAdminClass(session) {
    // 익명 사용자는 admin이 아님 — 이메일 있는 사용자(liakim)만
    const isAdmin = !!(session && session.user && !session.user.is_anonymous);
    document.body.classList.toggle('is-admin', isAdmin);
  }

  window.sb.auth.getSession().then(({ data: { session } }) => applyAdminClass(session));
  window.sb.auth.onAuthStateChange((_event, session) => applyAdminClass(session));

  // 로그아웃 링크 (있으면)
  document.addEventListener('click', async (e) => {
    const link = e.target.closest('#logoutLink');
    if (!link) return;
    e.preventDefault();
    if (!confirm('로그아웃 할까요?')) return;
    await window.sb.auth.signOut();
    location.reload();
  });
})();
