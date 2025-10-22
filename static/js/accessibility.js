(function () {
    const STORAGE_THEME_KEY = 'syssupport-theme';
    const STORAGE_FONT_KEY = 'syssupport-font-size';
    const fab = document.getElementById('accessibility-fab');
    const panel = document.getElementById('accessibility-panel');
    const themeButtons = document.querySelectorAll('.theme-toggle');
    const fontButtons = document.querySelectorAll('.font-toggle');
    const htmlEl = document.documentElement;
    const bodyEl = document.body;
    bodyEl.classList.add('text-base');

    function applyTheme(theme) {
        if (!['light', 'dark'].includes(theme)) {
            theme = 'light';
        }
        htmlEl.setAttribute('data-theme', theme);
        bodyEl.classList.toggle('bg-slate-100', theme === 'light');
        bodyEl.classList.toggle('bg-slate-900', theme === 'dark');
        bodyEl.classList.toggle('text-slate-900', theme === 'light');
        bodyEl.classList.toggle('text-slate-100', theme === 'dark');
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
        bodyEl.classList.remove('text-sm', 'text-base', 'text-lg');
        bodyEl.classList.add(`text-${size}`);
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
        bodyEl.classList.add(`text-${storedFont}`);
    }
})();
