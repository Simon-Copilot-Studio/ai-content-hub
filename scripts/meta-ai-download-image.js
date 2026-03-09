// Run via browser evaluate - downloads first scontent image as base64
// Returns { data: base64string, size: bytes }
async function downloadFirstImage() {
  const imgs = document.querySelectorAll('img[src*="scontent"]');
  if (imgs.length === 0) return { error: 'no images found' };
  const img = imgs[0];
  const resp = await fetch(img.src);
  const blob = await resp.blob();
  const reader = new FileReader();
  return new Promise(resolve => {
    reader.onloadend = () => {
      const b64 = reader.result.split(',')[1];
      resolve({ data: b64.substring(0, 50000), size: blob.size, total_b64_len: b64.length });
    };
    reader.readAsDataURL(blob);
  });
}
return downloadFirstImage();
