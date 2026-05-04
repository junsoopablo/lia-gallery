// === 방명록 (Supabase 기반) ===
// data-page 속성이 있는 .comments 섹션을 찾아서 댓글 로드/작성 처리
(function () {
  const SUPABASE_URL = 'https://qalprtpedzvnodbzwqih.supabase.co';
  const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhbHBydHBlZHp2bm9kYnp3cWloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc4NTYyMTgsImV4cCI6MjA5MzQzMjIxOH0.fWfs3wPU8OCQyPL2zDA5nb-H5TvoRs3EZRReUiEKlPw';

  const API = SUPABASE_URL + '/rest/v1';
  const HEADERS = {
    apikey: SUPABASE_ANON_KEY,
    Authorization: 'Bearer ' + SUPABASE_ANON_KEY
  };

  const section = document.querySelector('section.comments[data-page]');
  if (!section) return;

  const pageId = section.dataset.page;
  const list = section.querySelector('.comment-list');
  const form = section.querySelector('.comment-form');
  const status = section.querySelector('.comment-form-status');
  const submitBtn = form.querySelector('button[type=submit]');

  function timeAgo(iso) {
    const d = new Date(iso);
    const sec = (Date.now() - d.getTime()) / 1000;
    if (sec < 60) return '방금 전';
    if (sec < 3600) return Math.floor(sec / 60) + '분 전';
    if (sec < 86400) return Math.floor(sec / 3600) + '시간 전';
    if (sec < 604800) return Math.floor(sec / 86400) + '일 전';
    return d.getFullYear() + '년 ' + (d.getMonth() + 1) + '월 ' + d.getDate() + '일';
  }

  function renderList(comments) {
    list.innerHTML = '';
    if (!comments.length) {
      const empty = document.createElement('p');
      empty.className = 'comment-empty';
      empty.textContent = '아직 댓글이 없어요. 첫 댓글을 남겨주세요!';
      list.appendChild(empty);
      return;
    }
    const count = document.createElement('p');
    count.className = 'comment-count';
    count.textContent = `댓글 ${comments.length}개`;
    list.appendChild(count);

    comments.forEach(c => {
      const card = document.createElement('div');
      card.className = 'comment-card';

      const head = document.createElement('div');
      head.className = 'comment-head';
      const name = document.createElement('span');
      name.className = 'comment-name';
      name.textContent = c.name;
      const time = document.createElement('span');
      time.className = 'comment-time';
      time.textContent = timeAgo(c.created_at);
      head.appendChild(name);
      head.appendChild(time);

      const msg = document.createElement('p');
      msg.className = 'comment-message';
      msg.textContent = c.message;

      card.appendChild(head);
      card.appendChild(msg);
      list.appendChild(card);
    });
  }

  async function load() {
    try {
      const url = `${API}/comments?page=eq.${encodeURIComponent(pageId)}&select=*&order=created_at.desc&limit=200`;
      const res = await fetch(url, { headers: HEADERS });
      if (!res.ok) throw new Error('읽기 실패 (' + res.status + ')');
      const data = await res.json();
      renderList(data);
    } catch (e) {
      list.innerHTML = '';
      const err = document.createElement('p');
      err.className = 'comment-error';
      err.textContent = '댓글을 불러오지 못했어요: ' + e.message;
      list.appendChild(err);
    }
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = form.elements.name.value.trim();
    const message = form.elements.message.value.trim();
    if (!name || !message) return;
    submitBtn.disabled = true;
    status.textContent = '저장 중...';
    status.className = 'comment-form-status';
    try {
      const res = await fetch(`${API}/comments`, {
        method: 'POST',
        headers: {
          ...HEADERS,
          'Content-Type': 'application/json',
          Prefer: 'return=minimal'
        },
        body: JSON.stringify({ page: pageId, name, message })
      });
      if (!res.ok) throw new Error(await res.text());
      form.reset();
      status.textContent = '✓ 등록됐어요!';
      status.className = 'comment-form-status success';
      setTimeout(() => { status.textContent = ''; status.className = 'comment-form-status'; }, 3000);
      load();
    } catch (e) {
      status.textContent = '✗ 실패: ' + e.message;
      status.className = 'comment-form-status error';
    } finally {
      submitBtn.disabled = false;
    }
  });

  load();
})();
