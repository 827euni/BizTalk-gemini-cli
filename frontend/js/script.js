document.addEventListener('DOMContentLoaded', () => {
    const inputText = document.getElementById('inputText');
    const charCounter = document.getElementById('charCounter');
    const convertBtn = document.getElementById('convertBtn');
    const btnText = convertBtn.querySelector('.btn-text');
    const spinner = convertBtn.querySelector('.spinner');
    const outputText = document.getElementById('outputText');
    const copyBtn = document.getElementById('copyBtn');
    const feedbackMessage = document.getElementById('feedbackMessage');

    const MAX_CHARS = 500;

    // --- Event Listeners ---

    inputText.addEventListener('input', () => {
        const currentLength = inputText.value.length;
        charCounter.textContent = `${currentLength} / ${MAX_CHARS}`;
    });

    convertBtn.addEventListener('click', handleConvert);
    copyBtn.addEventListener('click', handleCopy);


    // --- Functions ---

    async function handleConvert() {
        const text = inputText.value.trim();
        const selectedTarget = document.querySelector('input[name="target"]:checked').value;

        if (!text) {
            showFeedback('내용을 입력해주세요.', 'error');
            return;
        }

        toggleLoading(true);

        try {
            // NOTE: 백엔드 app.py에 /api/convert 엔드포인트가 필요합니다.
            const response = await fetch('/api/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: text,
                    target: selectedTarget,
                }),
            });

            if (!response.ok) {
                throw new Error('서버에서 오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
            }

            const data = await response.json();
            
            // 백엔드 응답 형식에 따라 'data.converted_text'는 달라질 수 있습니다.
            outputText.textContent = data.converted_text || '결과를 받아오지 못했습니다.';
            copyBtn.disabled = false;

        } catch (error) {
            console.error('Conversion Error:', error);
            outputText.textContent = '';
            showFeedback(error.message, 'error');
            copyBtn.disabled = true;
        } finally {
            toggleLoading(false);
        }
    }

    function handleCopy() {
        const textToCopy = outputText.textContent;
        if (!textToCopy) return;

        navigator.clipboard.writeText(textToCopy).then(() => {
            showFeedback('복사되었습니다!', 'success');
        }).catch(err => {
            console.error('Copy Error:', err);
            showFeedback('복사에 실패했습니다.', 'error');
        });
    }

    function toggleLoading(isLoading) {
        if (isLoading) {
            convertBtn.disabled = true;
            btnText.style.display = 'none';
            spinner.style.display = 'block';
        } else {
            convertBtn.disabled = false;
            btnText.style.display = 'inline';
            spinner.style.display = 'none';
        }
    }

    function showFeedback(message, type) {
        feedbackMessage.textContent = message;
        feedbackMessage.className = 'show';
        feedbackMessage.classList.add(type);

        setTimeout(() => {
            feedbackMessage.className = '';
        }, 3000);
    }
});
