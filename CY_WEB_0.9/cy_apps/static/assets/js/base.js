// base.js
document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed'); // 用于调试，确认脚本执行

    // 搜索框功能
    initSearchBox();

    // 移动端菜单
    initMobileMenu();

    // 下拉菜单
    initDropdowns();

    // 导航栏阴影效果
    initNavShadow();

    // 平滑滚动
    initSmoothScroll();

    // 搜索功能
    initSearchFunction();

    // 下拉菜单宽度适配
    initDropdownWidth();
    const logoutLink = document.getElementById('logout-link');
    const logoutForm = document.getElementById('logout-form');
    const link = document.getElementById('logout-link');
    console.log(link); // 应输出 <a> 元素，而非 null
    if (!logoutLink) {
        console.error('错误：未找到退出登录链接，请检查HTML中的id="logout-link"');

    } else {
        console.error('you');
    }
    if (!logoutForm) {
        console.error('错误：未找到注销表单，请检查HTML中的id="logout-form"');

    }
    logoutLink.addEventListener('click', function (e) {
        e.preventDefault();
        if (confirm('确定要退出登录吗？')) {
            logoutForm.submit();
        }
    });


});

function initSearchBox() {
    const toggleBtn = document.getElementById("search-toggle");
    const searchBox = document.getElementById("search-box");
    const input = document.getElementById("search-input");

    if (!toggleBtn || !searchBox || !input) {
        console.warn('Search elements not found');
        return;
    }

    let searchOpen = false;
    let readyToClose = false;

    toggleBtn.addEventListener("click", () => {
        toggleBtn.classList.add("hidden");
        searchBox.classList.remove("opacity-0", "translate-x-full", "pointer-events-none", "w-0");
        searchBox.classList.add("opacity-100", "w-64");

        searchOpen = true;
        readyToClose = false;

        setTimeout(() => {
            input.focus();
            readyToClose = true;
        }, 300);
    });

    document.addEventListener("click", (e) => {
        if (searchOpen && readyToClose &&
            !searchBox.contains(e.target) &&
            !toggleBtn.contains(e.target)) {

            toggleBtn.classList.remove("hidden");
            searchBox.classList.add("opacity-0", "translate-x-full", "pointer-events-none", "w-0");
            searchBox.classList.remove("opacity-100", "w-64");

            searchOpen = false;
            readyToClose = false;
        }
    });

    document.addEventListener("keydown", (e) => {
        if (e.key === "Escape" && searchOpen && readyToClose) {
            toggleBtn.classList.remove("hidden");
            searchBox.classList.add("opacity-0", "translate-x-full", "pointer-events-none", "w-0");
            searchBox.classList.remove("opacity-100", "w-64");

            searchOpen = false;
            readyToClose = false;
        }
    });
}

function initMobileMenu() {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    if (!mobileMenuButton) return;

    mobileMenuButton.addEventListener('click', function () {
        const mobileMenu = document.getElementById('mobile-menu');
        if (mobileMenu) {
            mobileMenu.classList.toggle('hidden');
        }
    });

    // 移动端下拉菜单
    document.querySelectorAll('.mobile-dropdown-btn').forEach(button => {
        button.addEventListener('click', function () {
            const dropdown = this.nextElementSibling;
            if (dropdown) {
                dropdown.classList.toggle('hidden');

                // 切换图标
                const icon = this.querySelector('.fa-chevron-down');
                if (icon) {
                    if (dropdown.classList.contains('hidden')) {
                        icon.style.transform = 'rotate(0deg)';
                    } else {
                        icon.style.transform = 'rotate(180deg)';
                    }
                }
            }
        });
    });
}

function initDropdowns() {
    const dropdowns = document.querySelectorAll('.relative.group');

    dropdowns.forEach((dropdown, index) => {
        const btn = dropdown.querySelector('button');
        const menu = dropdown.querySelector('.dropdown-appear');
        const icon = dropdown.querySelector('.fa-chevron-down');

        // 跳过没有完整结构的下拉菜单
        if (!btn || !menu || !icon) return;

        // 初始隐藏菜单
        menu.classList.add('opacity-0', 'invisible', '-translate-y-2');

        // 点击按钮切换菜单显示
        btn.addEventListener('click', function (e) {
            e.stopPropagation();

            // 关闭其他所有菜单
            dropdowns.forEach(otherDropdown => {
                const otherBtn = otherDropdown.querySelector('button');
                const otherMenu = otherDropdown.querySelector('.dropdown-appear');
                const otherIcon = otherDropdown.querySelector('.fa-chevron-down');

                if (otherBtn !== btn && otherMenu && otherIcon) {
                    otherMenu.classList.remove('active');
                    otherMenu.classList.add('opacity-0', 'invisible', '-translate-y-2');
                    otherMenu.classList.remove('opacity-100', 'visible', 'translate-y-0');
                    otherIcon.classList.remove('rotate-180');
                }
            });

            // 切换当前菜单
            menu.classList.toggle('active');
            menu.classList.toggle('opacity-0');
            menu.classList.toggle('invisible');
            menu.classList.toggle('-translate-y-2');
            menu.classList.toggle('opacity-100');
            menu.classList.toggle('visible');
            menu.classList.toggle('translate-y-0');

            // 切换图标
            icon.classList.toggle('rotate-180');
        });
    });

    // 点击页面其他地方关闭所有菜单
    document.addEventListener('click', function () {
        dropdowns.forEach(dropdown => {
            const menu = dropdown.querySelector('.dropdown-appear');
            const icon = dropdown.querySelector('.fa-chevron-down');
            if (menu && icon && menu.classList.contains('active')) {
                menu.classList.remove('active');
                menu.classList.add('opacity-0', 'invisible', '-translate-y-2');
                menu.classList.remove('opacity-100', 'visible', 'translate-y-0');
                icon.classList.remove('rotate-180');
            }
        });
    });

    // 防止菜单内部点击关闭菜单
    document.querySelectorAll('.dropdown-appear').forEach(menu => {
        menu.addEventListener('click', function (e) {
            e.stopPropagation();
        });
    });
}

function initNavShadow() {
    window.addEventListener('scroll', function () {
        const nav = document.querySelector('nav');
        if (nav) {
            if (window.scrollY > 10) {
                nav.classList.add('shadow-lg');
            } else {
                nav.classList.remove('shadow-lg');
            }
        }
    });
}

function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // 考虑导航栏高度
                    behavior: 'smooth'
                });

                // 如果是移动端，点击后关闭菜单
                const mobileMenu = document.getElementById('mobile-menu');
                if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                    mobileMenu.classList.add('hidden');
                }
            }
        });
    });
}

function initSearchFunction() {
    const searchIcon = document.getElementById('search-icon');
    const searchInput = document.getElementById('search-input');

    if (searchIcon && searchInput) {
        // 图标点击事件：聚焦输入框并触发搜索
        searchIcon.addEventListener('click', function () {
            searchInput.focus();

            // 模拟搜索逻辑
            if (searchInput.value.trim()) {
                performSearch(searchInput.value);
            }
        });

        // 输入框回车触发搜索
        searchInput.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') {
                if (this.value.trim()) {
                    performSearch(this.value);
                }
            }
        });
    }

    // 搜索执行函数
    function performSearch(query) {
        console.log('搜索关键词:', query);
        // 这里可替换为实际的API请求或页面跳转逻辑
    }
}

function initDropdownWidth() {
    function setDropdownWidth() {
        const dropdownGroups = document.querySelectorAll('.group');

        dropdownGroups.forEach(group => {
            const dropdown = group.querySelector('.dropdown-appear');
            if (!dropdown) return;

            // 获取父容器宽度
            const containerWidth = group.getBoundingClientRect().width;

            // 应用宽度
            dropdown.style.setProperty('width', `${containerWidth}px`, 'important');
        });
    }

    // 初始化执行
    setTimeout(setDropdownWidth, 0); // 确保DOM完全加载

    // 窗口大小变化时更新
    window.addEventListener('resize', setDropdownWidth);

    // 监听DOM变化
    const observer = new MutationObserver(setDropdownWidth);
    const navElement = document.querySelector('nav');
    if (navElement) {
        observer.observe(navElement, {childList: true, subtree: true});
    }
}
