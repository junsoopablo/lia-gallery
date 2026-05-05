// Supabase 공통 설정. 여러 페이지에서 공유.
window.SUPABASE_URL = 'https://qalprtpedzvnodbzwqih.supabase.co';
window.SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFhbHBydHBlZHp2bm9kYnp3cWloIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzc4NTYyMTgsImV4cCI6MjA5MzQzMjIxOH0.fWfs3wPU8OCQyPL2zDA5nb-H5TvoRs3EZRReUiEKlPw';

window.imageUrl = function (imagePath) {
  return window.SUPABASE_URL + '/storage/v1/object/public/artworks/' + imagePath;
};
