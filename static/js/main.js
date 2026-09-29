document.documentElement.classList.add("js");

document.addEventListener("DOMContentLoaded", () => {
    const navbar = document.querySelector(".navbar");
    const updateNavbar = () => navbar?.classList.toggle("scrolled", window.scrollY > 12);
    updateNavbar();
    window.addEventListener("scroll", updateNavbar, { passive: true });

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealItems = document.querySelectorAll(".reveal");

    if (reducedMotion || !("IntersectionObserver" in window)) {
        revealItems.forEach((item) => item.classList.add("is-visible"));
    } else {
        const observer = new IntersectionObserver(
            (entries, revealObserver) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("is-visible");
                        revealObserver.unobserve(entry.target);
                    }
                });
            },
            { threshold: 0.12 }
        );
        revealItems.forEach((item) => observer.observe(item));
    }

    const navigation = document.querySelector("#mainNavigation");
    navigation?.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            const collapse = bootstrap.Collapse.getInstance(navigation);
            collapse?.hide();
        });
    });

    const subject = new URLSearchParams(window.location.search).get("subject");
    const subjectField = document.querySelector("#contactSubject");
    if (subject && subjectField && !subjectField.value) {
        subjectField.value = subject;
    }

    const contactForm = document.querySelector("#contactForm");
    contactForm?.addEventListener("submit", (event) => {
        event.preventDefault();
        if (!contactForm.reportValidity()) return;

        const fields = new FormData(contactForm);
        const recipient = contactForm.dataset.recipient;
        const emailSubject = fields.get("subject");
        const body = [
            `Name: ${fields.get("name")}`,
            `Email: ${fields.get("email")}`,
            `Organisation: ${fields.get("organisation") || "Not provided"}`,
            "",
            fields.get("message"),
        ].join("\n");

        window.location.href = `mailto:${recipient}?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(body)}`;
    });
});
