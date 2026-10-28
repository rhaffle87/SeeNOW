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

        const selectors = [
            'input[type="radio"]',
            'input[type="checkbox"]',
            'button',
            'a[href]',
            '[role="radio"]',
            '[role="checkbox"]',
            '[role="button"]',
            '[role="option"]',
            '.option',
            '.quiz-option',
            '.choice',
            '.choice-item',
            '.option-item',
            '.ant-radio-wrapper',
            '.ant-checkbox-wrapper',
            '.el-radio',
            '.el-checkbox',
            '.q-radio',
            '.q-checkbox',
            'label',
            '[onclick]'
        ];

        const allCandidates = querySelectorAllDeep(selectors.join(', '), document);

        const pointerElements = querySelectorAllDeep('div, span, li', document).filter(el => {
            const style = window.getComputedStyle(el);
            return style.cursor === 'pointer' && el.innerText && el.innerText.trim().length > 0 && el.innerText.length < 150;
        });

        const combined = [...allCandidates, ...pointerElements];

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

        const visibleElements = combined.filter(isVisible);

        const deduped = [];
        for (const el of visibleElements) {
            const rect = el.getBoundingClientRect();
            const isDuplicate = deduped.some(existing => {
                const exRect = existing.getBoundingClientRect();
                const centerDist = Math.hypot(
                    (rect.left + rect.width / 2) - (exRect.left + exRect.width / 2),
                    (rect.top + rect.height / 2) - (exRect.top + exRect.height / 2)
                );
                return centerDist < 12;
            });

            if (!isDuplicate) {
                deduped.push(el);
            }
        }

        const matchedElements = [];
        let index = 1;

        for (const el of deduped) {
            const rect = el.getBoundingClientRect();

            const box = document.createElement("div");
            box.style.position = "fixed";
            box.style.left = `${Math.round(rect.left)}px`;
            box.style.top = `${Math.round(rect.top)}px`;
            box.style.width = `${Math.round(rect.width)}px`;
            box.style.height = `${Math.round(rect.height)}px`;
            box.style.border = "2px solid #FF0055";
            box.style.boxSizing = "border-box";
            box.style.pointerEvents = "none";

            const badge = document.createElement("div");
            badge.innerText = `[${index}]`;
            badge.style.position = "absolute";
            badge.style.top = "-11px";
            badge.style.left = "0px";
            badge.style.backgroundColor = "#FFCC00";
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

            let textContent = (el.innerText || el.value || el.getAttribute("aria-label") || "").trim();
            textContent = textContent.replace(/\s+/g, " ").slice(0, 120);

            matchedElements.push({
                id: index,
                tag: el.tagName.toLowerCase(),
                type: el.getAttribute("type") || "",
                role: el.getAttribute("role") || "",
                text: textContent,
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
