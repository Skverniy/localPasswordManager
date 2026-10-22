/* Local Password Manager — frontend */

const API = "/api";
const appEl = document.getElementById("app");

const state = {
    initialized: false,
    authenticated: false,
    items: [],
};

/* ---------- HTTP ---------- */
async function api(path, opts = {}) {
    const res = await fetch(API + path, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        ...opts,
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
        if (res.status === 401) {
            state.authenticated = false;
        }
        throw new Error(data.detail || `HTTP ${res.status}`);
    }
    return data;
}

/* ---------- DOM helpers ---------- */
function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs || {})) {
        if (v == null || v === false) continue;
        if (k.startsWith("on")) {
            node.addEventListener(k.slice(2).toLowerCase(), v);
        } else if (k === "className") {
            node.className = v;
        } else if (k === "value") {
            node.value = v;
        } else {
            node.setAttribute(k, v);
        }
    }
    for (const child of children.flat()) {
        if (child == null || child === false) continue;
        node.appendChild(
            typeof child === "string" ? document.createTextNode(child) : child
        );
    }
    return node;
}

function clear(node) {
    while (node.firstChild) node.removeChild(node.firstChild);
}

function toast(msg, type = "info") {
    const colors = {
        error: "bg-red-600",
        success: "bg-emerald-600",
        info: "bg-slate-700",
    };
    const t = el(
        "div",
        {
            className: `fixed bottom-4 right-4 px-4 py-2 rounded shadow-lg text-white z-[100] ${colors[type] || colors.info}`,
        },
        msg
    );
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 2800);
}

/* ---------- Views ---------- */
function render() {
    clear(appEl);
    if (!state.initialized) return renderSetup();
    if (!state.authenticated) return renderLogin();
    return renderVault();
}

function renderSetup() {
    const form = el(
        "form",
        {
            className:
                "max-w-md mx-auto mt-20 bg-slate-800 p-8 rounded-lg shadow-lg space-y-3",
            onsubmit: async (e) => {
                e.preventDefault();
                const pw = form.querySelector("#pw").value;
                const pw2 = form.querySelector("#pw2").value;
                if (pw.length < 8) return toast("Минимум 8 символов", "error");
                if (pw !== pw2) return toast("Пароли не совпадают", "error");
                try {
                    await api("/auth/setup", {
                        method: "POST",
                        body: JSON.stringify({ master_password: pw }),
                    });
                    await doLogin(pw);
                    toast("Хранилище создано", "success");
                } catch (err) {
                    toast(err.message, "error");
                }
            },
        },
        el("h1", { className: "text-2xl font-bold" }, "Первый запуск"),
        el(
            "p",
            { className: "text-slate-400 text-sm" },
            "Задайте мастер-пароль. Восстановить его невозможно — храните надёжно."
        ),
        el("input", {
            id: "pw",
            type: "password",
            placeholder: "Мастер-пароль",
            className: "w-full p-3 rounded bg-slate-700 text-white",
            autofocus: "",
        }),
        el("input", {
            id: "pw2",
            type: "password",
            placeholder: "Повторите пароль",
            className: "w-full p-3 rounded bg-slate-700 text-white",
        }),
        el(
            "button",
            {
                type: "submit",
                className:
                    "w-full p-3 rounded bg-blue-600 hover:bg-blue-500 font-semibold transition",
            },
            "Создать хранилище"
        )
    );
    appEl.appendChild(form);
}

function renderLogin() {
    const form = el(
        "form",
        {
            className:
                "max-w-md mx-auto mt-20 bg-slate-800 p-8 rounded-lg shadow-lg space-y-3",
            onsubmit: async (e) => {
                e.preventDefault();
                const pw = form.querySelector("#pw").value;
                try {
                    await doLogin(pw);
                    toast("Добро пожаловать", "success");
                } catch (err) {
                    toast(err.message, "error");
                }
            },
        },
        el("h1", { className: "text-2xl font-bold" }, "Вход"),
        el("input", {
            id: "pw",
            type: "password",
            placeholder: "Мастер-пароль",
            className: "w-full p-3 rounded bg-slate-700 text-white",
            autofocus: "",
        }),
        el(
            "button",
            {
                type: "submit",
                className:
                    "w-full p-3 rounded bg-blue-600 hover:bg-blue-500 font-semibold transition",
            },
            "Войти"
        )
    );
    appEl.appendChild(form);
}

async function doLogin(password) {
    await api("/auth/login", {
        method: "POST",
        body: JSON.stringify({ master_password: password }),
    });
    state.authenticated = true;
    state.initialized = true;
    await loadItems();
    render();
}

async function loadItems() {
    state.items = await api("/vault/items");
}

function renderVault() {
    const wrap = el("div", { className: "space-y-4" });

    const header = el(
        "div",
        { className: "flex justify-between items-center gap-2 flex-wrap" },
        el("h1", { className: "text-2xl font-bold" }, "Хранилище"),
        el(
            "div",
            { className: "flex gap-2" },
            el(
                "button",
                {
                    className:
                        "px-4 py-2 rounded bg-blue-600 hover:bg-blue-500 font-semibold transition",
                    onclick: () => openEditor(null),
                },
                "+ Добавить"
            ),
            el(
                "button",
                {
                    className:
                        "px-4 py-2 rounded bg-red-600 hover:bg-red-500 transition",
                    onclick: async () => {
                        try {
                            await api("/auth/logout", { method: "POST" });
                        } catch {}
                        state.authenticated = false;
                        state.items = [];
                        render();
                    },
                },
                "Выйти"
            )
        )
    );
    wrap.appendChild(header);

    if (state.items.length === 0) {
        wrap.appendChild(
            el(
                "p",
                { className: "text-slate-400 text-center py-12" },
                "Пусто. Нажмите «Добавить», чтобы создать первую запись."
            )
        );
    } else {
        for (const item of state.items) wrap.appendChild(renderItem(item));
    }

    appEl.appendChild(wrap);
}

function renderItem(item) {
    const pwSpan = el("span", { className: "font-mono text-slate-400" }, "••••••••");
    let visible = false;

    const revealBtn = el(
        "button",
        {
            className: "text-sm text-blue-400 hover:text-blue-300",
            onclick: async () => {
                if (visible) {
                    pwSpan.textContent = "••••••••";
                    pwSpan.className = "font-mono text-slate-400";
                    visible = false;
                    revealBtn.textContent = "Показать";
                } else {
                    try {
                        const d = await api(`/vault/items/${item.id}/reveal`, {
                            method: "POST",
                        });
                        pwSpan.textContent = d.password;
                        pwSpan.className = "font-mono text-emerald-400 break-all";
                        visible = true;
                        revealBtn.textContent = "Скрыть";
                    } catch (err) {
                        toast(err.message, "error");
                    }
                }
            },
        },
        "Показать"
    );

    const copyBtn = el(
        "button",
        {
            className: "text-sm text-slate-400 hover:text-slate-200",
            onclick: async () => {
                try {
                    const d = await api(`/vault/items/${item.id}/reveal`, {
                        method: "POST",
                    });
                    await navigator.clipboard.writeText(d.password);
                    toast("Скопировано в буфер", "success");
                } catch (err) {
                    toast(err.message, "error");
                }
            },
        },
        "Копировать"
    );

    return el(
        "div",
        { className: "bg-slate-800 rounded-lg p-4 space-y-2" },
        el(
            "div",
            { className: "flex justify-between items-start gap-3" },
            el(
                "div",
                { className: "min-w-0" },
                el("div", { className: "font-semibold text-lg truncate" }, item.title),
                item.username &&
                    el("div", { className: "text-slate-400 text-sm truncate" }, item.username),
                item.url &&
                    el("div", { className: "text-slate-500 text-sm truncate" }, item.url)
            ),
            el(
                "div",
                { className: "flex gap-2 shrink-0" },
                el(
                    "button",
                    {
                        className: "text-sm text-slate-400 hover:text-slate-200",
                        onclick: () => openEditor(item),
                    },
                    "Изменить"
                ),
                el(
                    "button",
                    {
                        className: "text-sm text-red-400 hover:text-red-300",
                        onclick: async () => {
                            if (!confirm(`Удалить «${item.title}»?`)) return;
                            try {
                                await api(`/vault/items/${item.id}`, {
                                    method: "DELETE",
                                });
                                await loadItems();
                                render();
                                toast("Удалено", "success");
                            } catch (err) {
                                toast(err.message, "error");
                            }
                        },
                    },
                    "Удалить"
                )
            )
        ),
        el("div", { className: "flex items-center gap-3 flex-wrap" }, pwSpan, revealBtn, copyBtn),
        item.notes &&
            el(
                "div",
                {
                    className:
                        "text-slate-400 text-sm whitespace-pre-wrap border-t border-slate-700 pt-2",
                },
                item.notes
            )
    );
}

function openEditor(item) {
    const isNew = !item;
    const overlay = el("div", {
        className:
            "fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-50",
    });

    const form = el(
        "form",
        {
            className: "bg-slate-800 rounded-lg p-6 w-full max-w-md space-y-3",
            onsubmit: async (e) => {
                e.preventDefault();
                const data = {
                    title: form.querySelector("#f-title").value.trim(),
                    username: form.querySelector("#f-username").value,
                    url: form.querySelector("#f-url").value,
                    notes: form.querySelector("#f-notes").value,
                };
                const pw = form.querySelector("#f-password").value;
                if (isNew && !pw) return toast("Пароль обязателен", "error");
                if (pw) data.password = pw;

                try {
                    if (isNew) {
                        await api("/vault/items", {
                            method: "POST",
                            body: JSON.stringify(data),
                        });
                    } else {
                        await api(`/vault/items/${item.id}`, {
                            method: "PUT",
                            body: JSON.stringify(data),
                        });
                    }
                    overlay.remove();
                    await loadItems();
                    render();
                    toast(isNew ? "Создано" : "Обновлено", "success");
                } catch (err) {
                    toast(err.message, "error");
                }
            },
        },
        el("h2", { className: "text-xl font-bold" }, isNew ? "Новая запись" : "Редактировать"),
        el("input", {
            id: "f-title",
            placeholder: "Название *",
            required: "",
            value: item?.title || "",
            className: "w-full p-2 rounded bg-slate-700",
        }),
        el("input", {
            id: "f-username",
            placeholder: "Логин",
            value: item?.username || "",
            className: "w-full p-2 rounded bg-slate-700",
        }),
        el("input", {
            id: "f-url",
            placeholder: "URL",
            value: item?.url || "",
            className: "w-full p-2 rounded bg-slate-700",
        }),
        el("input", {
            id: "f-password",
            type: "password",
            placeholder: isNew ? "Пароль *" : "Новый пароль (пусто — не менять)",
            className: "w-full p-2 rounded bg-slate-700",
        }),
        el("textarea", {
            id: "f-notes",
            placeholder: "Заметки",
            rows: 3,
            value: item?.notes || "",
            className: "w-full p-2 rounded bg-slate-700",
        }),
        el(
            "div",
            { className: "flex gap-2 justify-end pt-2" },
            el(
                "button",
                {
                    type: "button",
                    className: "px-4 py-2 rounded bg-slate-600 hover:bg-slate-500",
                    onclick: () => overlay.remove(),
                },
                "Отмена"
            ),
            el(
                "button",
                {
                    type: "submit",
                    className:
                        "px-4 py-2 rounded bg-blue-600 hover:bg-blue-500 font-semibold",
                },
                "Сохранить"
            )
        )
    );

    overlay.appendChild(form);
    document.body.appendChild(overlay);
    form.querySelector("#f-title").focus();
}

/* ---------- Init ---------- */
(async function init() {
    try {
        const status = await api("/auth/status");
        state.initialized = !!status.initialized;
    } catch (err) {
        toast("Сервер недоступен", "error");
    }

    // Try to restore session
    if (state.initialized) {
        try {
            await loadItems();
            state.authenticated = true;
        } catch {
            state.authenticated = false;
        }
    }
    render();
})();