// core/som_injector.js
(() => {
    const OVERLAY_ID = "som-overlay-container";

    window.removeSoM = function(cleanAttributes = false) {
        const existing = document.getElementById(OVERLAY_ID);
        if (existing) {
            existing.remove();
        }
        if (cleanAttributes) {
            querySelectorAllDeep('[data-som-id]').forEach(el => el.removeAttribute('data-som-id'));
        }
    };

    function querySelectorAllDeep(selector, root = document) {
        const results = [];
        function collect(currentRoot) {
            if (!currentRoot) return;
            try {
                const elements = currentRoot.querySelectorAll(selector);
                for (let i = 0; i < elements.length; i++) {
                    results.push(elements[i]);
                }
            } catch(e) {}

            const allElements = currentRoot.querySelectorAll('*');
            for (let i = 0; i < allElements.length; i++) {
                if (allElements[i].shadowRoot) {
                    collect(allElements[i].shadowRoot);
                }
            }
        }
        collect(root);
        return Array.from(new Set(results));
    }

    window.injectSoM = function() {
        window.removeSoM(true);

        const overlay = document.createElement("div");
        overlay.id = OVERLAY_ID;
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100vw";
        overlay.style.height = "100vh";
        overlay.style.pointerEvents = "none";
        overlay.style.zIndex = "2147483647";
        document.body.appendChild(overlay);

        function isVisible(el) {
            if (!el) return false;
            const style = window.getComputedStyle(el);
            if (style.display === 'none' && el.tagName !== 'INPUT') return false;
            if (style.visibility === 'hidden') return false;
            if (parseFloat(style.opacity) === 0 && el.tagName !== 'INPUT') return false;

            const rect = el.getBoundingClientRect();
            if (rect.width <= 4 || rect.height <= 4) {
                if (el.tagName !== 'INPUT') return false;
            }
            if (rect.bottom < 0 || rect.top > window.innerHeight || rect.right < 0 || rect.left > window.innerWidth) {
                return false;
            }
            return true;
        }

        function isBlacklisted(el) {
            if (!el) return true;

            // 1. Blokir elemen di sidebar materi kursus, header, nav, switch-btn (ganti chapter), dan dialog AI
            if (el.closest('.catalog-tree, .catalog-tree-list, .menu-outer, .sidebar, .header-bar, .nav-bar, .v-step-target, .switch-btn, .course-bottom-nav, .chat-modal, .ai-assistant-modal')) {
                return true;
            }

            const rawText = (el.innerText || '').trim().toLowerCase();
            const className = (el.className && typeof el.className === 'string') ? el.className.toLowerCase() : '';

            // 2. Blokir tombol Mundur / Previous / Return / Exit secara permanen
            const backwardKeywords = ['previous', 'prev', 'sebelumnya', 'kembali', 'back', 'prv', 'return', 'return to course', 'return-score', 'goto-score', 'exit', 'keluar'];
            if (backwardKeywords.some(kw => rawText === kw || rawText.startsWith(kw + ' ') || className.includes(kw))) {
                return true;
            }

            // 3. Blokir widget Super AI / Assistant
            if (rawText.includes('super ai') || className.includes('super-ai') || className.includes('assistant')) {
                return true;
            }

            // 4. Blokir nomor palet soal kuis (tombol lompat nomor soal 1-60 di sheet item)
            if (/^\\d{1,3}$/.test(rawText)) {
                if (el.tagName !== 'INPUT' && !className.includes('option') && !el.closest('.option-list-item, .quiz-option, .choice')) {
                    return true;
                }
            }

            // 5. Blokir item palet sheet dan pagination
            if (className.includes('sheet-item') || className.includes('card-item') || className.includes('question-card-item') || className.includes('pagination') || className.includes('pager')) {
                return true;
            }

            return false;
        }

        function checkIsSelected(element) {
            if (!element) return false;

            // 1. Native input
            if (element.tagName === 'INPUT' && (element.checked || element.getAttribute('aria-checked') === 'true')) {
                return true;
            }
            if (element.getAttribute('aria-checked') === 'true') {
                return true;
            }

            // 2. Cek class checked spesifik platform (Huawei, Element UI, Ant Design, Quasar, Vue, Tailwind)
            const checkedClasses = [
                'kltcourse-checkbox-checked',
                'kltcourse-checkbox-wrapper-checked',
                'kltcourse-radio-checked',
                'kltcourse-radio-wrapper-checked',
                'ant-checkbox-checked',
                'ant-radio-checked',
                'is-checked',
                'is-selected',
                'is-active'
            ];

            const selfCls = (element.className && typeof element.className === 'string') ? element.className.toLowerCase() : '';
            if (checkedClasses.some(c => selfCls.includes(c))) {
                return true;
            }

            // 3. Cek apakah ada child di dalam elemen yang memiliki class checked
            for (const c of checkedClasses) {
                if (element.querySelector && element.querySelector(`[class*="${c}"]`)) {
                    return true;
                }
            }

            // 4. Cek class checked generik
            if (element.querySelector && element.querySelector('[class*="-checked"]')) {
                return true;
            }

            // 5. Cek child input
            const childInput = element.querySelector ? element.querySelector('input[type="radio"], input[type="checkbox"]') : null;
            if (childInput && (childInput.checked || childInput.getAttribute('aria-checked') === 'true')) {
                return true;
            }

            return false;
        }

        // --- STEP 1: DETEKSI OPSI KUIS SECARA KANONIKAL (1 OPSI = 1 ID) ---
        const optionContainerSelectors = [
            '.option-list-item',
            '.quiz-option',
            '.choice-item',
            '.option-item',
            '.question-choice',
            '.kltCourse-radio-wrapper',
            '.kltCourse-checkbox-wrapper',
            '.ant-radio-wrapper',
            '.ant-checkbox-wrapper',
            'label.el-radio',
            'label.el-checkbox',
            '[role="radio"]',
            '[role="checkbox"]'
        ];

        const rawContainers = querySelectorAllDeep(optionContainerSelectors.join(', '), document)
            .filter(el => isVisible(el) && !isBlacklisted(el));

        // Bersihkan duplikasi container bertingkat (ambil container terluar per opsi)
        const canonicalOptionContainers = [];
        for (const c of rawContainers) {
            const hasParentContainer = canonicalOptionContainers.some(existing => existing.contains(c));
            if (!hasParentContainer) {
                // Buang container yang ada di dalam c jika c lebih luar
                for (let i = canonicalOptionContainers.length - 1; i >= 0; i--) {
                    if (c.contains(canonicalOptionContainers[i])) {
                        canonicalOptionContainers.splice(i, 1);
                    }
                }
                canonicalOptionContainers.push(c);
            }
        }

        const optionCandidates = [];
        for (const container of canonicalOptionContainers) {
            // Pilih elemen klik terbaik: label klik jika ada, atau container itu sendiri
            const clickable = container.querySelector('label.option-list') || 
                              container.querySelector('label') || 
                              container;
            optionCandidates.push({
                element: clickable,
                container: container,
                isOption: true
            });
        }

        // --- STEP 2: DETEKSI TOMBOL AKSI KUIS (NEXT / SUBMIT) ---
        const actionSelectors = [
            '.subject-btn',
            'button',
            'a[role="button"]',
            '[role="button"]',
            '.ant-btn',
            '.el-button',
            'input[type="submit"]',
            'input[type="button"]'
        ];

        const rawActions = querySelectorAllDeep(actionSelectors.join(', '), document)
            .filter(el => isVisible(el) && !isBlacklisted(el));

        // Tambahkan div/span yang berperilaku seperti tombol teks utama
        const textActionCandidates = querySelectorAllDeep('div, span', document).filter(el => {
            if (!isVisible(el) || isBlacklisted(el)) return false;
            const t = (el.innerText || '').trim().toLowerCase();
            return ['next', 'submit', 'selanjutnya', 'kirim', 'finish', 'selesai', 'lanjut'].includes(t);
        });

        const combinedActions = [...rawActions, ...textActionCandidates];
        const canonicalActions = [];

        for (const act of combinedActions) {
            // Abaikan jika aksi berada di dalam container opsi kuis
            if (canonicalOptionContainers.some(opt => opt.contains(act))) continue;

            // Abaikan container induk yang membungkus banyak tombol (contoh .subject-btns)
            if (act.querySelectorAll('.subject-btn, button, [role="button"]').length > 1) continue;

            // Hindari duplikasi parent-child untuk tombol yang sama (ambil elemen tombol terdalam atau tombol yang punya class tombol)
            const hasExisting = canonicalActions.some(existing => existing === act || existing.contains(act) || act.contains(existing));
            if (!hasExisting) {
                canonicalActions.push(act);
            }
        }

        // --- STEP 3: GABUNGKAN & BERIKAN BADGE SET-OF-MARKS ---
        const finalItemList = [];
        for (const opt of optionCandidates) {
            finalItemList.push({
                element: opt.element,
                container: opt.container,
                isOption: true
            });
        }
        for (const act of canonicalActions) {
            finalItemList.push({
                element: act,
                container: act,
                isOption: false
            });
        }

        const matchedElements = [];
        let index = 1;

        for (const item of finalItemList) {
            const el = item.element;
            const container = item.container;
            const rect = el.getBoundingClientRect();

            const box = document.createElement("div");
            box.style.position = "fixed";
            box.style.left = `${Math.round(rect.left)}px`;
            box.style.top = `${Math.round(rect.top)}px`;
            box.style.width = `${Math.round(rect.width)}px`;
            box.style.height = `${Math.round(rect.height)}px`;
            box.style.border = item.isOption ? "2px solid #00E5FF" : "2px solid #FF0055";
            box.style.boxSizing = "border-box";
            box.style.pointerEvents = "none";

            const badge = document.createElement("div");
            badge.innerText = `[${index}]`;
            badge.style.position = "absolute";
            badge.style.top = "-11px";
            badge.style.left = "0px";
            badge.style.backgroundColor = item.isOption ? "#00E5FF" : "#FFCC00";
            badge.style.color = "#000000";
            badge.style.fontSize = "11px";
            badge.style.fontWeight = "900";
            badge.style.fontFamily = "monospace";
            badge.style.padding = "0px 3px";
            badge.style.borderRadius = "2px";
            badge.style.border = "1px solid #000000";
            badge.style.lineHeight = "1.1";
            badge.style.zIndex = "2147483647";

            box.appendChild(badge);
            overlay.appendChild(box);

            el.setAttribute("data-som-id", index.toString());

            let textContent = (item.isOption ? container.innerText : (el.innerText || el.value || el.getAttribute("aria-label") || "")).trim();
            textContent = textContent.replace(/\\s+/g, " ").slice(0, 140);

            matchedElements.push({
                id: index,
                tag: el.tagName.toLowerCase(),
                type: el.getAttribute("type") || "",
                role: el.getAttribute("role") || "",
                text: textContent,
                is_checked: checkIsSelected(container),
                rect: {
                    x: Math.round(rect.left),
                    y: Math.round(rect.top),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                }
            });

            index++;
        }

        return matchedElements;
    };
})();
