const modules = {
  'ATZ-NAV-001': './library/navegacion/ATZ-NAV-001.js',
  'ATZ-SEC-004': './library/secciones/ATZ-SEC-004.js',
  'ATZ-SEC-007': './library/secciones/ATZ-SEC-007.js',
};

for (const [id, file] of Object.entries(modules)) {
  const element = document.querySelector(`[data-atz-id="${id}"]`);
  if (!element) continue;
  import(file).then(({ mount }) => {
    if (id !== 'ATZ-SEC-004') return mount(element);
    const narrow = matchMedia('(max-width: 760px)');
    const scene = mount(element, { reduced: narrow.matches });
    narrow.addEventListener('change', event => scene.setReduced(event.matches));
    return scene;
  }).catch(error => {
    console.error(`APEL: ${id}`, error);
  });
}

if (window.AtrezzoTransitions) {
  new window.AtrezzoTransitions({
    defaultEffect: 'split',
    coverColor: '#643608',
    coverMs: 480,
    revealMs: 560,
    showLabel: false,
  });
}

const gallery = document.querySelector('[data-gallery]');
if (gallery) {
  const dialog = gallery.querySelector('dialog');
  const photo = dialog.querySelector('img');
  let trigger = null;
  gallery.addEventListener('click', event => {
    const anchor = event.target.closest('[data-gallery-photo]');
    if (!anchor || event.defaultPrevented || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    trigger = anchor;
    photo.src = anchor.href;
    photo.alt = anchor.querySelector('img').alt;
    dialog.showModal();
  });
  dialog.addEventListener('close', () => trigger?.focus());
}

const studio = document.querySelector('[data-studio]');
if (studio) {
  const pieces = Array.from(studio.querySelectorAll('[data-piece]'));
  const choose = studio.querySelector('[data-piece-select]');
  const palette = studio.querySelector('[data-colour-select]');
  const diagram = studio.querySelector('svg');

  function setColour(piece) {
    piece.setAttribute('fill', palette.value);
  }

  choose.addEventListener('change', () => {
    palette.value = pieces[Number(choose.value)].getAttribute('fill');
  });
  palette.addEventListener('change', () => setColour(pieces[Number(choose.value)]));
  studio.querySelector('[data-apply-all]').addEventListener('click', () => pieces.forEach(setColour));
  studio.querySelector('[data-reset]').addEventListener('click', () => {
    palette.selectedIndex = 0;
    choose.selectedIndex = 0;
    pieces.forEach(setColour);
  });
  studio.querySelector('[data-export]').addEventListener('click', () => {
    const blob = new Blob([new XMLSerializer().serializeToString(diagram)], { type: 'image/svg+xml' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'apel-ligas.svg';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  });
}
