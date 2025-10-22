(function () {
    const canvas = document.getElementById('signature-pad');
    const clearBtn = document.getElementById('clear-signature');
    const form = document.getElementById('finalizacao-form');
    const hiddenInput = form ? form.querySelector('input[name="assinatura_data"]') : null;

    if (!canvas || !form || !hiddenInput || typeof SignaturePad === 'undefined') {
        return;
    }

    const signaturePad = new SignaturePad(canvas, {
        minWidth: 1,
        maxWidth: 3,
        penColor: '#111827',
        backgroundColor: 'rgba(255,255,255,0)',
    });

    function resizeCanvas() {
        const ratio = Math.max(window.devicePixelRatio || 1, 1);
        canvas.width = canvas.offsetWidth * ratio;
        canvas.height = canvas.offsetHeight * ratio;
        canvas.getContext('2d').scale(ratio, ratio);
        signaturePad.clear();
    }

    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();

    clearBtn.addEventListener('click', function () {
        signaturePad.clear();
        hiddenInput.value = '';
    });

    form.addEventListener('submit', function (event) {
        if (signaturePad.isEmpty()) {
            event.preventDefault();
            alert('A assinatura é obrigatória.');
            return false;
        }
        hiddenInput.value = signaturePad.toDataURL('image/png');
        return true;
    });
})();
