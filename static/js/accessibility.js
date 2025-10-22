(function () {
    const STORAGE_THEME_KEY = 'syssupport-theme';
    const STORAGE_FONT_KEY = 'syssupport-font-size';
    const fab = document.getElementById('accessibility-fab');
    const panel = document.getElementById('accessibility-panel');
    const themeButtons = document.querySelectorAll('.theme-toggle');
    const fontButtons = document.querySelectorAll('.font-toggle');
    const htmlEl = document.documentElement;
    const bodyEl = document.body;
    // Garante que só uma classe de fonte fique ativa
    function setFontSizeClass(size) {
        bodyEl.classList.remove('text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl');
        // Mais perceptível: xs, base, xl
        if (size === 'sm') {
            bodyEl.classList.add('text-xs');
        } else if (size === 'base') {
            bodyEl.classList.add('text-base');
        } else if (size === 'lg') {
            bodyEl.classList.add('text-xl');
        }
    }

    setFontSizeClass('base');

    function applyTheme(theme) {
        if (!['light', 'dark'].includes(theme)) {
            theme = 'light';
        }
        htmlEl.setAttribute('data-theme', theme);
        // Limpa classes antigas
        bodyEl.classList.remove('bg-slate-100', 'bg-slate-900', 'text-slate-900', 'text-slate-100');
        // Aplica tema
        if (theme === 'light') {
            bodyEl.classList.add('bg-slate-100', 'text-slate-900');
        } else {
            bodyEl.classList.add('bg-slate-900', 'text-slate-100');
        }
        // Ajusta contraste de elementos principais
        document.querySelectorAll('.bg-white').forEach(el => {
            if (theme === 'dark') {
                el.classList.add('bg-slate-800');
                el.classList.remove('bg-white');
            } else {
                el.classList.add('bg-white');
                el.classList.remove('bg-slate-800');
            }
        });
        document.querySelectorAll('.text-slate-800, .text-slate-700, .text-slate-600, .text-slate-500').forEach(el => {
            if (theme === 'dark') {
                el.classList.add('text-slate-100');
                el.classList.remove('text-slate-800', 'text-slate-700', 'text-slate-600', 'text-slate-500');
            } else {
                el.classList.remove('text-slate-100');
                // Não reverte para todos, mas mantém contraste
            }
        });
        localStorage.setItem(STORAGE_THEME_KEY, theme);
    }

    function applyFontSize(action) {
        const sizes = ['sm', 'base', 'lg'];
        let current = localStorage.getItem(STORAGE_FONT_KEY) || 'base';
        let index = sizes.indexOf(current);
        if (action === 'increase' && index < sizes.length - 1) {
            index += 1;
        } else if (action === 'decrease' && index > 0) {
            index -= 1;
        } else if (action === 'reset') {
            index = sizes.indexOf('base');
        }
        const size = sizes[index];
        bodyEl.dataset.fontSize = size;
        setFontSizeClass(size);
        localStorage.setItem(STORAGE_FONT_KEY, size);
    }

    function togglePanel() {
        if (!panel) return;
        panel.classList.toggle('hidden');
    }

    function handleOutsideClick(event) {
        if (!panel || panel.classList.contains('hidden')) return;
        if (event.target === panel || panel.contains(event.target) || event.target === fab) {
            return;
        }
        panel.classList.add('hidden');
    }

    if (fab) {
        fab.addEventListener('click', togglePanel);
    }

    themeButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const selectedTheme = event.currentTarget.dataset.theme;
            applyTheme(selectedTheme);
        });
    });

    fontButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const action = event.currentTarget.dataset.font;
            applyFontSize(action);
        });
    });

    document.addEventListener('click', handleOutsideClick);

    // Initialize with saved preferences
    const storedTheme = localStorage.getItem(STORAGE_THEME_KEY);
    const storedFont = localStorage.getItem(STORAGE_FONT_KEY);
    if (storedTheme) {
        applyTheme(storedTheme);
    }
    if (storedFont) {
        bodyEl.dataset.fontSize = storedFont;
        setFontSizeClass(storedFont);
    }
})();
