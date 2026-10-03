/**
 * EduRAG Merdeka — Landing Page Interactive Engine
 * WCAG 2.2 AA Accessible, Zero Framework Dependencies, High Performance
 */

document.addEventListener('DOMContentLoaded', () => {
  initThemeEngine();
  initAppBarElevation();
  initGitHubStars();
  initModeSwitcher();
  initInteractiveDemo();
  initQuickstartCopy();
  initFAQAccordion();
  initContributors();
});

/* --------------------------------------------------------------------------
   1. M3 Theme Engine (Light / Dark with LocalStorage & OS Sync)
   -------------------------------------------------------------------------- */
function initThemeEngine() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const htmlEl = document.documentElement;

  // Retrieve saved preference or check OS preference
  const savedTheme = localStorage.getItem('edurag-theme');
  const systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const initialTheme = savedTheme || (systemPrefersDark ? 'dark' : 'light');

  applyTheme(initialTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = htmlEl.getAttribute('data-theme') || 'light';
      const newTheme = currentTheme === 'light' ? 'dark' : 'light';
      applyTheme(newTheme);
      localStorage.setItem('edurag-theme', newTheme);
    });
  }

  // Listen to OS theme changes if user hasn't explicitly set preference
  window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
    if (!localStorage.getItem('edurag-theme')) {
      applyTheme(e.matches ? 'dark' : 'light');
    }
  });

  function applyTheme(theme) {
    htmlEl.setAttribute('data-theme', theme);
    if (themeIcon) {
      themeIcon.textContent = theme === 'dark' ? 'light_mode' : 'dark_mode';
    }
  }
}

/* --------------------------------------------------------------------------
   2. Top App Bar Elevation on Scroll
   -------------------------------------------------------------------------- */
function initAppBarElevation() {
  const appBar = document.getElementById('app-bar');
  if (!appBar) return;

  const handleScroll = () => {
    if (window.scrollY > 20) {
      appBar.classList.add('elevated');
    } else {
      appBar.classList.remove('elevated');
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  handleScroll();
}

/* --------------------------------------------------------------------------
   3. Live GitHub Star Count with Graceful Fallback
   -------------------------------------------------------------------------- */
async function initGitHubStars() {
  const starCountEl = document.getElementById('repo-stars');
  if (!starCountEl) return;

  try {
    const res = await fetch('https://api.github.com/repos/indri007/eduragmerdeka');
    if (!res.ok) throw new Error('API rate limited or unavailable');
    const data = await res.json();
    if (typeof data.stargazers_count === 'number') {
      starCountEl.textContent = data.stargazers_count.toString();
    }
  } catch (err) {
    // Graceful fallback to static value
    console.debug('GitHub star fetch notice:', err.message);
  }
}

/* --------------------------------------------------------------------------
   4. Mode Siswa vs Mode Guru (Segmented Switcher)
   -------------------------------------------------------------------------- */
function initModeSwitcher() {
  const btnSiswa = document.getElementById('btn-mode-siswa');
  const btnGuru = document.getElementById('btn-mode-guru');
  const viewSiswa = document.getElementById('view-siswa');
  const viewGuru = document.getElementById('view-guru');

  if (!btnSiswa || !btnGuru || !viewSiswa || !viewGuru) return;

  btnSiswa.addEventListener('click', () => {
    btnSiswa.classList.add('active');
    btnSiswa.setAttribute('aria-selected', 'true');
    btnGuru.classList.remove('active');
    btnGuru.setAttribute('aria-selected', 'false');

    viewSiswa.classList.add('active');
    viewGuru.classList.remove('active');
  });

  btnGuru.addEventListener('click', () => {
    btnGuru.classList.add('active');
    btnGuru.setAttribute('aria-selected', 'true');
    btnSiswa.classList.remove('active');
    btnSiswa.setAttribute('aria-selected', 'false');

    viewGuru.classList.add('active');
    viewSiswa.classList.remove('active');
  });
}

/* --------------------------------------------------------------------------
   5. Interactive Simulation / Sandbox Playground
   -------------------------------------------------------------------------- */
function initInteractiveDemo() {
  const form = document.getElementById('demo-form');
  const inputField = document.getElementById('demo-input-field');
  const chatContainer = document.getElementById('demo-chat-container');
  const chips = document.querySelectorAll('.demo-chip');

  if (!form || !inputField || !chatContainer) return;

  // Pre-configured authentic knowledge base responses for demo
  const mockResponses = {
    'eksponen': {
      text: 'Eksponen adalah bentuk perkalian berulang dari suatu bilangan pokok yang sama (aⁿ = a × a × ... × a sebanyak n kali). Sedangkan logaritma adalah operasi inversi (kebalikan) dari eksponen, yaitu mencari nilai pangkat jika basis dan hasil pemangkatannya diketahui (ᵃlog b = c ⇔ aᶜ = b).',
      citation: 'Matematika Kelas 10 • Bab 1 Eksponen & Logaritma • Halaman 14',
      similarity: 0.94
    },
    'observasi': {
      text: 'Struktur teks Laporan Hasil Observasi (LHO) terdiri dari 3 bagian utama: (1) Pernyataan Umum/Klasifikasi (definisi dan pengenalan objek), (2) Deskripsi Bagian (rincian detail objek yang diamati), dan (3) Deskripsi Manfaat atau Kesimpulan.',
      citation: 'Bahasa Indonesia Kelas 10 • Bab 1 Mengungkap Fakta Alam • Halaman 9',
      similarity: 0.92
    },
    'pemanasan global': {
      text: 'Pemanasan global dipicu oleh efek rumah kaca akibat akumulasi gas CO₂, CH₄, dan N₂O di atmosfer. Gas-gas ini memerangkap radiasi gelombang panjang inframerah yang dipantulkan bumi, sehingga temperatur rata-rata atmosfer dan lautan meningkat secara gradual.',
      citation: 'IPA Terpadu Kelas 10 • Bab 8 Pemanasan Global: Konsep dan Solusi • Halaman 184',
      similarity: 0.89
    },
    'vektor': {
      text: 'Vektor adalah besaran yang memiliki nilai dan arah. Dalam sistem koordinat kartesius dua dimensi, vektor dapat dinyatakan dalam kombinasi linear vektor satuan <strong>u = xi + yj</strong> dengan panjang vektor |u| = √(x² + y²).',
      citation: 'Matematika Kelas 10 • Bab 2 Vektor dan Operasinya • Halaman 48',
      similarity: 0.91
    },
    'trap': {
      isTrap: true,
      text: 'Materi tidak ditemukan di buku Kurikulum Merdeka Kelas 10, coba kata kunci lain terkait pelajaran resmi.',
      similarity: 0.23
    }
  };

  chips.forEach(chip => {
    chip.addEventListener('click', () => {
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const query = chip.getAttribute('data-query');
      if (query) {
        inputField.value = query;
        handleQuerySubmit(query);
      }
    });
  });

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const query = inputField.value.trim();
    if (query) {
      handleQuerySubmit(query);
    }
  });

  function handleQuerySubmit(query) {
    // Append User Bubble
    const userBubble = document.createElement('div');
    userBubble.className = 'mini-chat-bubble user';
    userBubble.textContent = query;
    chatContainer.appendChild(userBubble);
    inputField.value = '';

    // Scroll to bottom
    chatContainer.scrollTop = chatContainer.scrollHeight;

    // Simulate AI Retrieval & Guardrail Processing
    const typingBubble = document.createElement('div');
    typingBubble.className = 'mini-chat-bubble ai';
    typingBubble.innerHTML = '<span style="opacity: 0.6;">🔍 Mengambil konteks dari Buku Kurikulum Merdeka (Qdrant top-k)...</span>';
    chatContainer.appendChild(typingBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;

    setTimeout(() => {
      typingBubble.remove();
      renderAIResponse(query);
    }, 700);
  }

  function renderAIResponse(query) {
    const qLower = query.toLowerCase();
    let match = null;

    if (qLower.includes('piala dunia') || qLower.includes('2030') || qLower.includes('presiden') || qLower.includes('resep')) {
      match = mockResponses['trap'];
    } else if (qLower.includes('eksponen') || qLower.includes('logaritma')) {
      match = mockResponses['eksponen'];
    } else if (qLower.includes('observasi') || qLower.includes('struktur')) {
      match = mockResponses['observasi'];
    } else if (qLower.includes('pemanasan') || qLower.includes('iklim') || qLower.includes('suhu')) {
      match = mockResponses['pemanasan global'];
    } else if (qLower.includes('vektor')) {
      match = mockResponses['vektor'];
    } else {
      // Generic match with citation
      match = {
        text: `Berdasarkan Buku Siswa Kurikulum Merdeka Kelas 10, topik "${escapeHTML(query)}" dibahas dalam konteks capaian pembelajaran fase E. Seluruh konsep diarahkan pada pemahaman inkuiri dan pemecahan masalah kontekstual.`,
        citation: 'Kurikulum Merdeka Kelas 10 • Panduan Belajar • Hal. 24',
        similarity: 0.81
      };
    }

    const aiBubble = document.createElement('div');
    aiBubble.className = 'mini-chat-bubble ai';

    if (match.isTrap) {
      aiBubble.innerHTML = `
        <div style="color: var(--md-sys-color-error); font-weight: 700; margin-bottom: 4px;">
          🛡️ Guardrail Anti-Halusinasi Terpicu
        </div>
        ${match.text}
        <div class="mini-badge" style="background: var(--md-sys-color-error-container); color: var(--md-sys-color-on-error-container); margin-top: 6px;">
          Cosine Similarity: ${match.similarity} (&lt; 0.70 Ambang Batas)
        </div>
      `;
    } else {
      aiBubble.innerHTML = `
        <div>${match.text}</div>
        <div style="margin-top: 10px; padding-top: 8px; border-top: 1px dashed var(--md-sys-color-outline-variant); font-size: 0.75rem; color: var(--md-sys-color-tertiary); font-weight: 600;">
          🏷️ Sitasi Resmi: ${match.citation}
        </div>
        <div class="mini-badge" style="background: var(--md-sys-color-primary-container); color: var(--md-sys-color-on-primary-container); margin-top: 6px;">
          Cosine Similarity: ${match.similarity} (&gt; 0.70 Lolos)
        </div>
      `;
    }

    chatContainer.appendChild(aiBubble);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, tag => ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      "'": '&#39;',
      '"': '&quot;'
    }[tag] || tag));
  }
}

/* --------------------------------------------------------------------------
   6. Quick Start Terminal Copy Button
   -------------------------------------------------------------------------- */
function initQuickstartCopy() {
  const copyBtn = document.getElementById('copy-quickstart');
  const copyText = document.getElementById('copy-btn-text');

  if (!copyBtn) return;

  const codeSnippet = `git clone https://github.com/indri007/eduragmerdeka.git\ncd eduragmerdeka\npython3 -m venv venv && source venv/bin/activate\npip install -r requirements.txt\nstreamlit run app.py`;

  copyBtn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(codeSnippet);
      if (copyText) copyText.textContent = 'Tersalin!';
      copyBtn.style.borderColor = 'var(--md-sys-color-primary)';
      setTimeout(() => {
        if (copyText) copyText.textContent = 'Salin';
        copyBtn.style.borderColor = '';
      }, 2000);
    } catch (e) {
      console.warn('Clipboard copy failed:', e);
    }
  });
}

/* --------------------------------------------------------------------------
   7. FAQ Accordion (Keyboard & Screen Reader Accessible)
   -------------------------------------------------------------------------- */
function initFAQAccordion() {
  const faqItems = document.querySelectorAll('.faq-item');

  faqItems.forEach(item => {
    const questionBtn = item.querySelector('.faq-question');
    if (!questionBtn) return;

    questionBtn.addEventListener('click', () => {
      const isOpen = item.classList.contains('open');

      // Close other items
      faqItems.forEach(i => {
        i.classList.remove('open');
        const btn = i.querySelector('.faq-question');
        if (btn) btn.setAttribute('aria-expanded', 'false');
      });

      // Toggle clicked item
      if (!isOpen) {
        item.classList.add('open');
        questionBtn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/* --------------------------------------------------------------------------
   8. Contributor Avatars Fetcher
   -------------------------------------------------------------------------- */
async function initContributors() {
  const container = document.getElementById('contributors-container');
  if (!container) return;

  try {
    const res = await fetch('https://api.github.com/repos/indri007/eduragmerdeka/contributors');
    if (!res.ok) throw new Error('API rate limit');
    const contributors = await res.json();

    if (Array.isArray(contributors) && contributors.length > 0) {
      container.innerHTML = contributors.map(c => `
        <a href="${c.html_url}" target="_blank" rel="noopener noreferrer" style="text-decoration: none; color: inherit; display: flex; align-items: center; gap: 8px; background: var(--md-sys-color-surface-container-high); padding: 6px 14px; border-radius: var(--md-sys-shape-corner-full); border: 1px solid var(--md-sys-color-outline-variant); transition: transform 0.2s ease;">
          <img src="${c.avatar_url}" alt="${c.login}" style="width: 28px; height: 28px; border-radius: 50%;">
          <span style="font-weight: 600; font-size: 0.875rem;">${c.login}</span>
        </a>
      `).join('');
    }
  } catch (err) {
    // Keep fallback author already present in HTML
  }
}
