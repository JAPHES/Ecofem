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
    const subjectField = document.querySelector("#id_subject");
    if (subject && subjectField && !subjectField.value) {
        subjectField.value = subject;
    }
});
