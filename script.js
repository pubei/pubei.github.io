"use strict";
var UserStatus;
(function (UserStatus) {
    UserStatus["LoggedIn"] = "Logged In";
    UserStatus["LoggingIn"] = "Logging In";
    UserStatus["LoggedOut"] = "Logged Out";
    UserStatus["LogInError"] = "Log In Error";
    UserStatus["VerifyingLogIn"] = "Verifying Log In";
})(UserStatus || (UserStatus = {}));
var Default;
(function (Default) {
    Default["PIN"] = "1234";
})(Default || (Default = {}));
var WeatherType;
(function (WeatherType) {
    WeatherType["Cloudy"] = "Cloudy";
    WeatherType["Rainy"] = "Rainy";
    WeatherType["Stormy"] = "Stormy";
    WeatherType["Sunny"] = "Sunny";
})(WeatherType || (WeatherType = {}));
const defaultPosition = () => ({
    left: 0,
    x: 0
});
const N = {
    clamp: (min, value, max) => Math.min(Math.max(min, value), max),
    rand: (min, max) => Math.floor(Math.random() * (max - min + 1) + min)
};
const T = {
    format: (date) => {
        const hours = T.formatHours(date.getHours()), minutes = date.getMinutes(), seconds = date.getSeconds();
        return `${hours}:${T.formatSegment(minutes)}`;
    },
    formatHours: (hours) => {
        return hours % 12 === 0 ? 12 : hours % 12;
    },
    formatSegment: (segment) => {
        return segment < 10 ? `0${segment}` : segment;
    }
};
const LogInUtility = {
    verify: async (pin) => {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                if (pin === Default.PIN) {
                    resolve(true);
                }
                else {
                    reject(`Invalid pin: ${pin}`);
                }
            }, N.rand(300, 700));
        });
    }
};
const useCurrentDateEffect = () => {
    const [date, setDate] = React.useState(new Date());
    React.useEffect(() => {
        const interval = setInterval(() => {
            const update = new Date();
            if (update.getSeconds() !== date.getSeconds()) {
                setDate(update);
            }
        }, 100);
        return () => clearInterval(interval);
    }, [date]);
    return date;
};
const RouterContext = React.createContext(null);
const useRouter = () => React.useContext(RouterContext);
const RouterProvider = ({ children }) => {
    const [route, setRouteTo] = React.useState(() => {
        return window.location.hash.slice(1) || '/';
    });
    React.useEffect(() => {
        const handleHashChange = () => {
            setRouteTo(window.location.hash.slice(1) || '/');
        };
        window.addEventListener('hashchange', handleHashChange);
        return () => window.removeEventListener('hashchange', handleHashChange);
    }, []);
    const navigate = (path) => {
        window.location.hash = path;
    };
    return React.createElement(RouterContext.Provider, { value: { route, navigate } }, children);
};
const ScrollableComponent = (props) => {
    const ref = React.useRef(null);
    const [state, setStateTo] = React.useState({
        grabbing: false,
        position: defaultPosition()
    });
    const handleOnMouseDown = (e) => {
        setStateTo(Object.assign(Object.assign({}, state), { grabbing: true, position: {
                x: e.clientX,
                left: ref.current.scrollLeft
            } }));
    };
    const handleOnMouseMove = (e) => {
        if (state.grabbing) {
            const left = Math.max(0, state.position.left + (state.position.x - e.clientX));
            ref.current.scrollLeft = left;
        }
    };
    const handleOnMouseUp = () => {
        if (state.grabbing) {
            setStateTo(Object.assign(Object.assign({}, state), { grabbing: false }));
        }
    };
    return (React.createElement("div", { ref: ref, className: classNames("scrollable-component", props.className), id: props.id, onMouseDown: handleOnMouseDown, onMouseMove: handleOnMouseMove, onMouseUp: handleOnMouseUp, onMouseLeave: handleOnMouseUp }, props.children));
};
const WeatherSnap = () => {
    const [temperature] = React.useState(N.rand(65, 85));
    return (React.createElement("span", { className: "weather" },
        React.createElement("i", { className: "weather-type", className: "fa-duotone fa-sun" }),
        React.createElement("span", { className: "weather-temperature-value" }, temperature),
        React.createElement("span", { className: "weather-temperature-unit" }, "\u00B0F")));
};
const Reminder = () => {
    return (React.createElement("div", { className: "reminder" },
        React.createElement("span", { className: "reminder-text" }, "欢迎使用您的智能家居")));
};
const Time = () => {
    const date = useCurrentDateEffect();
    return (React.createElement("span", { className: "time" }, T.format(date)));
};
const Info = (props) => {
    return (React.createElement("div", { id: props.id, className: "info" },
        React.createElement(Time, null),
        React.createElement(WeatherSnap, null)));
};
const PinDigit = (props) => {
    const [hidden, setHiddenTo] = React.useState(false);
    React.useEffect(() => {
        if (props.value) {
            const timeout = setTimeout(() => {
                setHiddenTo(true);
            }, 500);
            return () => {
                setHiddenTo(false);
                clearTimeout(timeout);
            };
        }
    }, [props.value]);
    return (React.createElement("div", { className: classNames("app-pin-digit", { focused: props.focused, hidden }) },
        React.createElement("span", { className: "app-pin-digit-value" }, props.value || "")));
};
const Pin = () => {
    const { userStatus, setUserStatusTo } = React.useContext(AppContext);
    const [pin, setPinTo] = React.useState("");
    const ref = React.useRef(null);
    React.useEffect(() => {
        if (userStatus === UserStatus.LoggingIn || userStatus === UserStatus.LogInError) {
            ref.current.focus();
        }
        else {
            setPinTo("");
        }
    }, [userStatus]);
    React.useEffect(() => {
        if (pin.length === 4) {
            const verify = async () => {
                try {
                    setUserStatusTo(UserStatus.VerifyingLogIn);
                    if (await LogInUtility.verify(pin)) {
                        setUserStatusTo(UserStatus.LoggedIn);
                    }
                }
                catch (err) {
                    console.error(err);
                    setUserStatusTo(UserStatus.LogInError);
                }
            };
            verify();
        }
        if (userStatus === UserStatus.LogInError) {
            setUserStatusTo(UserStatus.LoggingIn);
        }
    }, [pin]);
    const handleOnClick = () => {
        ref.current.focus();
    };
    const handleOnCancel = () => {
        setUserStatusTo(UserStatus.LoggedOut);
    };
    const handleOnChange = (e) => {
        if (e.target.value.length <= 4) {
            setPinTo(e.target.value.toString());
        }
    };
    const getCancelText = () => {
        return (React.createElement("span", { id: "app-pin-cancel-text", onClick: handleOnCancel }, "取消"));
    };
    const getErrorText = () => {
        if (userStatus === UserStatus.LogInError) {
            return (React.createElement("span", { id: "app-pin-error-text" }, "无效的PIN码"));
        }
    };
    return (React.createElement("div", { id: "app-pin-wrapper" },
        React.createElement("input", { disabled: userStatus !== UserStatus.LoggingIn && userStatus !== UserStatus.LogInError, id: "app-pin-hidden-input", maxLength: 4, ref: ref, type: "number", value: pin, onChange: handleOnChange }),
        React.createElement("div", { id: "app-pin", onClick: handleOnClick },
            React.createElement(PinDigit, { focused: pin.length === 0, value: pin[0] }),
            React.createElement(PinDigit, { focused: pin.length === 1, value: pin[1] }),
            React.createElement(PinDigit, { focused: pin.length === 2, value: pin[2] }),
            React.createElement(PinDigit, { focused: pin.length === 3, value: pin[3] })),
        React.createElement("h3", { id: "app-pin-label" },
            "输入PIN码 (1234) ",
            getErrorText(),
            " ",
            getCancelText())));
};
const MenuSection = (props) => {
    const getContent = () => {
        if (props.scrollable) {
            return (React.createElement(ScrollableComponent, { className: "menu-section-content" }, props.children));
        }
        return (React.createElement("div", { className: "menu-section-content" }, props.children));
    };
    return (React.createElement("div", { id: props.id, className: "menu-section" },
        React.createElement("div", { className: "menu-section-title" },
            React.createElement("i", { className: props.icon }),
            React.createElement("span", { className: "menu-section-title-text" }, props.title)),
        getContent()));
};
const QuickNav = () => {
    const getItems = () => {
        return [{
                id: 1,
                label: "智能家居"
            }, {
                id: 2,
                label: "温度调节"
            }, {
                id: 3,
                label: "全屋灯光"
            }, {
                id: 4,
                label: "晚安模式"
            }].map((item) => {
            return (React.createElement("div", { key: item.id, className: "quick-nav-item clear-button" },
                React.createElement("span", { className: "quick-nav-item-label" }, item.label)));
        });
    };
    return (React.createElement(ScrollableComponent, { id: "quick-nav" }, getItems()));
};
const Weather = () => {
    const getDays = () => {
        return [{
                id: 1,
                name: "周一",
                temperature: N.rand(60, 80),
                weather: WeatherType.Sunny
            }, {
                id: 2,
                name: "周二",
                temperature: N.rand(60, 80),
                weather: WeatherType.Sunny
            }, {
                id: 3,
                name: "周三",
                temperature: N.rand(60, 80),
                weather: WeatherType.Cloudy
            }, {
                id: 4,
                name: "周四",
                temperature: N.rand(60, 80),
                weather: WeatherType.Rainy
            }, {
                id: 5,
                name: "周五",
                temperature: N.rand(60, 80),
                weather: WeatherType.Stormy
            }, {
                id: 6,
                name: "周六",
                temperature: N.rand(60, 80),
                weather: WeatherType.Sunny
            }, {
                id: 7,
                name: "周日",
                temperature: N.rand(60, 80),
                weather: WeatherType.Cloudy
            }].map((day) => {
            const getIcon = () => {
                switch (day.weather) {
                    case WeatherType.Cloudy:
                        return "fa-duotone fa-clouds";
                    case WeatherType.Rainy:
                        return "fa-duotone fa-cloud-drizzle";
                    case WeatherType.Stormy:
                        return "fa-duotone fa-cloud-bolt";
                    case WeatherType.Sunny:
                        return "fa-duotone fa-sun";
                }
            };
            return (React.createElement("div", { key: day.id, className: "day-card" },
                React.createElement("div", { className: "day-card-content" },
                    React.createElement("span", { className: "day-weather-temperature" },
                        day.temperature,
                        React.createElement("span", { className: "day-weather-temperature-unit" }, "\u00B0F")),
                    React.createElement("i", { className: classNames("day-weather-icon", getIcon(), day.weather.toLowerCase()) }),
                    React.createElement("span", { className: "day-name" }, day.name))));
        });
    };
    return (React.createElement(MenuSection, { icon: "fa-solid fa-sun", id: "weather-section", scrollable: true, title: "今日天气如何？" }, getDays()));
};
const Tools = () => {
    const getTools = () => {
        return [{
                icon: "fa-solid fa-air-conditioner",
                id: 1,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/1.jpg",
                label: "已连接",
                name: "空调"
            }, {
                icon: "fa-solid fa-vent-damper",
                id: 2,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/2.jpg",
                label: "空气净化器",
                name: "已连接"
            }, {
                icon: "fa-solid fa-tv",
                id: 3,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/3.jpg",
                label: "控制",
                name: "Apple TV"
            }, {
                icon: "fa-solid fa-battery-bolt",
                id: 4,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/4.jpg?compress=1&resize=800x600&vertical=top",
                label: "公用事业",
                name: "能源使用"
            }, {
                icon: "fa-solid fa-router",
                id: 5,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/5.jpg",
                label: "网络",
                name: "Wifi"
            }, {
                icon: "fa-solid fa-speaker",
                id: 6,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/6.jpg",
                label: "音频",
                name: "家庭音响"
            }].map((tool) => {
            const styles = {
                backgroundImage: `url(${tool.image})`
            };
            return (React.createElement("div", { key: tool.id, className: "tool-card" },
                React.createElement("div", { className: "tool-card-background background-image", style: styles }),
                React.createElement("div", { className: "tool-card-content" },
                    React.createElement("div", { className: "tool-card-content-header" },
                        React.createElement("span", { className: "tool-card-label" }, tool.label),
                        React.createElement("span", { className: "tool-card-name" }, tool.name)),
                    React.createElement("i", { className: classNames(tool.icon, "tool-card-icon") }))));
        });
    };
    return (React.createElement(MenuSection, { icon: "fa-solid fa-rectangles-mixed", id: "tools-section", title: "其他控制" }, getTools()));
};
const Restaurants = () => {
    const getRestaurants = () => {
        return [{
                desc: "灯光",
                id: 1,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/7.jpg",
                title: "客厅"
            }, {
                desc: "灯光",
                id: 2,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/8.jpg",
                title: "主卧室"
            }, {
                desc: "灯光",
                id: 3,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/9.jpg",
                title: "厨房"
            }, {
                desc: "灯光",
                id: 4,
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/10.jpg",
                title: "书房"
            }].map((restaurant) => {
            const styles = {
                backgroundImage: `url(${restaurant.image})`
            };
            return (React.createElement("div", { key: restaurant.id, className: "restaurant-card background-image", style: styles },
                React.createElement("div", { className: "restaurant-card-content" },
                    React.createElement("div", { className: "restaurant-card-content-items" },
                        React.createElement("span", { className: "restaurant-card-title" }, restaurant.title),
                        React.createElement("span", { className: "restaurant-card-desc" }, restaurant.desc)))));
        });
    };
    return (React.createElement(MenuSection, { icon: "fa-regular fa-lightbulb", id: "restaurants-section", title: "家庭灯光控制" }, getRestaurants()));
};
const Movies = () => {
    const getMovies = () => {
        return [{
                desc: "仪表盘统计",
                id: 1,
                icon: "fa-solid fa-battery-full",
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/11.jpg",
                title: "Tesla Powerwall"
            }, {
                desc: "能源生产",
                id: 2,
                icon: "fa-solid fa-solar-panel",
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/12.jpg",
                title: "太阳能发电"
            }, {
                desc: "电动车充电统计",
                id: 3,
                icon: "fa-solid fa-charging-station",
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/13.jpg",
                title: "充电站"
            }, {
                desc: "家庭安全概览",
                id: 4,
                icon: "fa-solid fa-camera-security",
                image: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/14.jpg",
                title: "家庭安全系统"
            }].map((movie) => {
            const styles = {
                backgroundImage: `url(${movie.image})`
            };
            const id = `movie-card-${movie.id}`;
            return (React.createElement("div", { key: movie.id, id: id, className: "movie-card" },
                React.createElement("div", { className: "movie-card-background background-image", style: styles }),
                React.createElement("div", { className: "movie-card-content" },
                    React.createElement("div", { className: "movie-card-info" },
                        React.createElement("span", { className: "movie-card-title" }, movie.title),
                        React.createElement("span", { className: "movie-card-desc" }, movie.desc)),
                    React.createElement("i", { className: movie.icon }))));
        });
    };
    return (React.createElement(MenuSection, { icon: "fa-solid fa-battery-bolt", id: "movies-section", scrollable: true, title: "其他仪表盘" }, getMovies()));
};
const UserStatusButton = (props) => {
    const { userStatus, setUserStatusTo } = React.useContext(AppContext);
    const handleOnClick = () => {
        setUserStatusTo(props.userStatus);
    };
    return (React.createElement("button", { id: props.id, className: "user-status-button clear-button", disabled: userStatus === props.userStatus, type: "button", onClick: handleOnClick },
        React.createElement("i", { className: props.icon })));
};
const Navigation = () => {
    const [isHidden, setIsHidden] = React.useState(false);
    const { route, navigate } = useRouter();
    const scrollTimeoutRef = React.useRef(null);
    React.useEffect(() => {
        const handleScroll = () => {
            setIsHidden(true);
            if (scrollTimeoutRef.current) {
                clearTimeout(scrollTimeoutRef.current);
            }
            scrollTimeoutRef.current = setTimeout(() => {
                setIsHidden(false);
            }, 1000);
        };
        window.addEventListener('scroll', handleScroll);
        return () => {
            window.removeEventListener('scroll', handleScroll);
            if (scrollTimeoutRef.current) {
                clearTimeout(scrollTimeoutRef.current);
            }
        };
    }, []);
    const navLinks = [
        { label: '首页', path: '/' },
        { label: '公司介绍', path: '/about' },
        { label: '全屋定制', path: '/custom' },
        { label: '案例展示', path: '/cases' },
        { label: '在线预约', path: '/booking' },
        { label: '关于我们', path: '/contact' }
    ];
    return (React.createElement("div", { id: "app-navbar", className: classNames({ hidden: isHidden }) },
        React.createElement("div", { id: "app-navbar-logo" },
            React.createElement("img", { id: "app-navbar-logo-image", src: "https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/logo.png", alt: "Logo" }),
            React.createElement("span", { id: "app-navbar-logo-text" }, "浦北装修设计")),
        React.createElement("div", { id: "app-navbar-links" }, navLinks.map((link) => (React.createElement("span", { key: link.path, className: classNames("app-navbar-link", { active: route === link.path }), onClick: () => navigate(link.path) }, link.label)))));
};
const Menu = () => {
    return (React.createElement("div", { id: "app-menu" },
        React.createElement("div", { id: "app-menu-content-wrapper" },
            React.createElement("div", { id: "app-menu-content" },
                React.createElement("div", { id: "app-menu-content-header" },
                    React.createElement("div", { className: "app-menu-content-header-section" },
                        React.createElement(Info, { id: "app-menu-info" }),
                        React.createElement(Reminder, null)),
                    React.createElement("div", { className: "app-menu-content-header-section" },
                        React.createElement(UserStatusButton, { icon: "fa-solid fa-arrow-right", id: "sign-out-button", userStatus: UserStatus.LoggedOut }))),
                React.createElement(QuickNav, null),
                React.createElement(Weather, null),
                React.createElement(Restaurants, null),
                React.createElement(Tools, null),
                React.createElement(Movies, null)))));
};
const Background = () => {
    const { userStatus, setUserStatusTo } = React.useContext(AppContext);
    const handleOnClick = () => {
        if (userStatus === UserStatus.LoggedOut) {
            setUserStatusTo(UserStatus.LoggingIn);
        }
    };
    return (React.createElement("div", { id: "app-background", onClick: handleOnClick },
        React.createElement("div", { id: "app-background-image", className: "background-image" })));
};
const Loading = () => {
    return (React.createElement("div", { id: "app-loading-icon" },
        React.createElement("i", { className: "fa-solid fa-spinner-third" })));
};
const AboutPage = () => {
    return React.createElement("div", { className: "page-content" },
        React.createElement("div", { className: "page-section" },
            React.createElement("h2", null, "公司介绍"),
            React.createElement("p", null, "浦北装修设计有限公司成立于2010年，是一家专注于高端家居设计与全屋定制的专业机构。"),
            React.createElement("p", null, "我们拥有经验丰富的设计团队，致力于为客户提供个性化、高品质的家居解决方案。从空间规划到细节设计，从材料选择到施工监理，我们全程把控每一个环节，确保交付完美的作品。")),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "我们的理念"),
            React.createElement("ul", null,
                React.createElement("li", null, "以客户需求为核心，创造舒适宜居的空间"),
                React.createElement("li", null, "坚持原创设计，拒绝千篇一律"),
                React.createElement("li", null, "注重环保材料，守护家人健康"),
                React.createElement("li", null, "精益求精，追求卓越品质"))),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "团队实力"),
            React.createElement("p", null, "公司现有设计团队20余人，平均从业经验超过10年，多次获得行业设计大奖。")));
};
const CustomPage = () => {
    return React.createElement("div", { className: "page-content" },
        React.createElement("div", { className: "page-section" },
            React.createElement("h2", null, "全屋定制"),
            React.createElement("p", null, "我们提供一站式全屋定制服务，涵盖厨房、卧室、客厅、书房等各个空间。")),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "定制流程"),
            React.createElement("div", { className: "process-steps" },
                React.createElement("div", { className: "process-step" },
                    React.createElement("i", { className: "fa-solid fa-pencil" }),
                    React.createElement("span", null, "免费咨询")),
                React.createElement("div", { className: "process-step" },
                    React.createElement("i", { className: "fa-solid fa-ruler-combined" }),
                    React.createElement("span", null, "上门测量")),
                React.createElement("div", { className: "process-step" },
                    React.createElement("i", { className: "fa-solid fa-desktop" }),
                    React.createElement("span", null, "方案设计")),
                React.createElement("div", { className: "process-step" },
                    React.createElement("i", { className: "fa-solid fa-hammer" }),
                    React.createElement("span", null, "施工安装")),
                React.createElement("div", { className: "process-step" },
                    React.createElement("i", { className: "fa-solid fa-check-circle" }),
                    React.createElement("span", null, "验收交付")))),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "定制优势"),
            React.createElement("ul", null,
                React.createElement("li", null, "个性化设计，满足独特需求"),
                React.createElement("li", null, "环保板材，E0级标准"),
                React.createElement("li", null, "专业安装团队，确保质量"),
                React.createElement("li", null, "5年质保，终身维护"))));
};
const CasesPage = () => {
    return React.createElement("div", { className: "page-content" },
        React.createElement("div", { className: "page-section" },
            React.createElement("h2", null, "案例展示"),
            React.createElement("p", null, "精选优质案例，展示不同风格的设计作品"))),
        React.createElement("div", { className: "cases-grid" },
            React.createElement("div", { className: "case-card" },
                React.createElement("div", { className: "case-card-image", style: { backgroundImage: 'url(https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/7.jpg)' } }),
                React.createElement("div", { className: "case-card-content" },
                    React.createElement("h4", null, "现代简约风格"),
                    React.createElement("p", null, "客厅设计案例"))),
            React.createElement("div", { className: "case-card" },
                React.createElement("div", { className: "case-card-image", style: { backgroundImage: 'url(https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/8.jpg)' } }),
                React.createElement("div", { className: "case-card-content" },
                    React.createElement("h4", null, "北欧风格"),
                    React.createElement("p", null, "主卧室设计案例"))),
            React.createElement("div", { className: "case-card" },
                React.createElement("div", { className: "case-card-image", style: { backgroundImage: 'url(https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/9.jpg)' } }),
                React.createElement("div", { className: "case-card-content" },
                    React.createElement("h4", null, "新中式风格"),
                    React.createElement("p", null, "厨房设计案例"))),
            React.createElement("div", { className: "case-card" },
                React.createElement("div", { className: "case-card-image", style: { backgroundImage: 'url(https://raw.githubusercontent.com/pubei/pubei.github.io/refs/heads/main/image/10.jpg)' } }),
                React.createElement("div", { className: "case-card-content" },
                    React.createElement("h4", null, "轻奢风格"),
                    React.createElement("p", null, "书房设计案例")))));
};
const BookingPage = () => {
    const [formData, setFormData] = React.useState({
        name: '',
        phone: '',
        email: '',
        type: 'design',
        message: ''
    });
    const [submitted, setSubmitted] = React.useState(false);
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };
    const handleSubmit = (e) => {
        e.preventDefault();
        setSubmitted(true);
    };
    if (submitted) {
        return React.createElement("div", { className: "page-content" },
            React.createElement("div", { className: "page-section" },
                React.createElement("h2", null, "预约成功"),
                React.createElement("p", null, "感谢您的预约，我们的设计师将在24小时内与您联系。")));
    }
    return React.createElement("div", { className: "page-content" },
        React.createElement("div", { className: "page-section" },
            React.createElement("h2", null, "在线预约"),
            React.createElement("p", null, "填写以下信息，我们将为您安排专业的设计咨询服务")),
        React.createElement("div", { className: "page-section" },
            React.createElement("form", { onSubmit: handleSubmit, className: "booking-form" },
                React.createElement("div", { className: "form-group" },
                    React.createElement("label", null, "姓名"),
                    React.createElement("input", { type: "text", name: "name", value: formData.name, onChange: handleChange, required: true })),
                React.createElement("div", { className: "form-group" },
                    React.createElement("label", null, "电话"),
                    React.createElement("input", { type: "tel", name: "phone", value: formData.phone, onChange: handleChange, required: true })),
                React.createElement("div", { className: "form-group" },
                    React.createElement("label", null, "邮箱"),
                    React.createElement("input", { type: "email", name: "email", value: formData.email, onChange: handleChange })),
                React.createElement("div", { className: "form-group" },
                    React.createElement("label", null, "服务类型"),
                    React.createElement("select", { name: "type", value: formData.type, onChange: handleChange },
                        React.createElement("option", { value: "design" }, "设计咨询"),
                        React.createElement("option", { value: "custom" }, "全屋定制"),
                        React.createElement("option", { value: "renovation" }, "装修施工"),
                        React.createElement("option", { value: "consult" }, "免费测量"))),
                React.createElement("div", { className: "form-group" },
                    React.createElement("label", null, "留言"),
                    React.createElement("textarea", { name: "message", value: formData.message, onChange: handleChange, rows: 4 })),
                React.createElement("button", { type: "submit", className: "submit-button" }, "提交预约"))));
};
const ContactPage = () => {
    return React.createElement("div", { className: "page-content" },
        React.createElement("div", { className: "page-section" },
            React.createElement("h2", null, "关于我们"),
            React.createElement("p", null, "浦北装修设计有限公司，您身边的家居设计专家"))),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "联系方式"),
            React.createElement("div", { className: "contact-info" },
                React.createElement("div", { className: "contact-item" },
                    React.createElement("i", { className: "fa-solid fa-map-marker-alt" }),
                    React.createElement("span", null, "广西浦北县小江街道xxx路xxx号")),
                React.createElement("div", { className: "contact-item" },
                    React.createElement("i", { className: "fa-solid fa-phone" }),
                    React.createElement("span", null, "0777-xxx-xxxx")),
                React.createElement("div", { className: "contact-item" },
                    React.createElement("i", { className: "fa-solid fa-mobile-screen" }),
                    React.createElement("span", null, "138-xxxx-xxxx")),
                React.createElement("div", { className: "contact-item" },
                    React.createElement("i", { className: "fa-solid fa-envelope" }),
                    React.createElement("span", null, "contact@pubei-design.com")))),
        React.createElement("div", { className: "page-section" },
            React.createElement("h3", null, "营业时间"),
            React.createElement("p", null, "周一至周六：09:00 - 18:00"),
            React.createElement("p", null, "周日：10:00 - 17:00"))));
};
const AppContext = React.createContext(null);
const App = () => {
    const [userStatus, setUserStatusTo] = React.useState(UserStatus.LoggedOut);
    const { route } = useRouter();
    const getStatusClass = () => {
        return userStatus.replace(/\s+/g, "-").toLowerCase();
    };
    const showNavbar = () => {
        return userStatus === UserStatus.LoggedIn;
    };
    const renderPage = () => {
        switch (route) {
            case '/about':
                return React.createElement(AboutPage, null);
            case '/custom':
                return React.createElement(CustomPage, null);
            case '/cases':
                return React.createElement(CasesPage, null);
            case '/booking':
                return React.createElement(BookingPage, null);
            case '/contact':
                return React.createElement(ContactPage, null);
            default:
                return React.createElement(Menu, null);
        }
    };
    return (React.createElement(RouterProvider, null,
        React.createElement(AppContext.Provider, { value: { userStatus, setUserStatusTo } },
            React.createElement("div", { id: "app", className: getStatusClass() },
                showNavbar() && React.createElement(Navigation, null),
                React.createElement(Info, { id: "app-info" }),
                React.createElement(Pin, null),
                renderPage(),
                React.createElement(Background, null),
                React.createElement("div", { id: "sign-in-button-wrapper" },
                    React.createElement(UserStatusButton, { icon: "fa-solid fa-arrow-right", id: "sign-in-button", userStatus: UserStatus.LoggingIn })),
                React.createElement(Loading, null)))));
};
ReactDOM.render(React.createElement(App, null), document.getElementById("root"));

/*
  Inspired by: "Error, 404"
  By: Sujeet Mishra
  Link: https://dribbble.com/shots/4571035-Error-404
*/

let oh = document.querySelector('.circle.oh');

document.addEventListener('mousemove', event => {
  let domainX = [0, document.body.clientWidth],
  domainY = [0, document.body.clientHeight],
  range = [-10, 10];

  let translate = {
    x: range[0] + (event.clientX - domainX[0]) * (range[1] - range[0]) / (domainX[1] - domainX[0]),
    y: range[0] + (event.clientY - domainY[0]) * (range[1] - range[0]) / (domainY[1] - domainY[0]) };


  oh.style.animation = 'none';
  oh.style.transform = `translate(${translate.x}px, ${translate.y}px)`;
});

document.addEventListener('mouseleave', event => {
  oh.style.animation = 'floating 3s linear infinite';
});