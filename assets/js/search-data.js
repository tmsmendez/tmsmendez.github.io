// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "About",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-research",
          title: "Research",
          description: "Selected research....",
          section: "Navigation",
          handler: () => {
            window.location.href = "/research/";
          },
        },{id: "nav-publications",
          title: "Publications",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/publications/";
          },
        },{id: "nav-projects",
          title: "Projects",
          description: "Selected projects, pavilions and demonstrators.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "dropdown-bookshelf",
              title: "bookshelf",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/books/";
              },
            },{id: "dropdown-blog",
              title: "blog",
              description: "",
              section: "Dropdown",
              handler: () => {
                window.location.href = "/blog/";
              },
            },{id: "news-appointed-assistant-professor-at-the-uw-department-of-architecture",
          title: 'Appointed Assistant Professor at the UW Department of Architecture',
          description: "",
          section: "News",},{id: "news-prof-méndez-echenagucia-awarded-a-uw-royalty-research-fund-grant",
          title: 'Prof. Méndez Echenagucia awarded a UW Royalty Research Fund grant',
          description: "",
          section: "News",},{id: "news-former-student-vidhya-rajendran-recieves-2020-asa-meeting-best-student-paper",
          title: 'Former student Vidhya Rajendran recieves 2020 ASA Meeting best student paper',
          description: "",
          section: "News",},{id: "news-new-article-by-fast-company-on-our-helmholtz-resonator-panels",
          title: 'New Article by Fast company on our Helmholtz Resonator panels',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2021-9-19.html";
            },},{id: "news-the-hilo-unit-has-been-officially-opened",
          title: 'The Hilo Unit has been officially opened',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2021-10-6.html";
            },},{id: "news-prof-méndez-echenagucia-named-one-of-2021-most-creative-people-by-fast-company",
          title: 'Prof. Méndez Echenagucia named one of 2021 Most creative people by Fast Company...',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2021-10-8.html";
            },},{id: "news-nathan-brown-and-vidhya-rajendran-present-our-work-at-asa-2021-seattle",
          title: 'Nathan Brown and Vidhya Rajendran present our work at ASA 2021 Seattle',
          description: "",
          section: "News",},{id: "news-new-paper-out-on-jasa-on-the-design-of-thin-helmholtz-resonators",
          title: 'New paper out on JASA on the design of thin Helmholtz Resonators',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2022-1-26.html";
            },},{id: "news-uw-team-is-receives-arpa-e-grant",
          title: 'UW Team is receives ARPA-e grant',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2022-3-31.html";
            },},{id: "news-energy-and-buildings-paper-published",
          title: 'Energy and Buildings paper published',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2022-11-3.html";
            },},{id: "news-the-hilo-unit-receives-the-2022-arc-award",
          title: 'The HiLo unit receives the 2022 ARC award',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2022-11-6.html";
            },},{id: "news-aia-seattle-award-of-merit",
          title: 'AIA Seattle Award of Merit',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2022-11-7.html";
            },},{id: "news-new-conference-paper-accepted-for-asce-2023",
          title: 'New conference paper accepted for ASCE 2023!',
          description: "",
          section: "News",},{id: "news-new-conference-paper-accepted-for-eurodyn-2023-at-tu-delft",
          title: 'New conference paper accepted for EURODYN 2023 at TU Delft!',
          description: "",
          section: "News",},{id: "news-new-conference-paper-accepted-in-forum-acusticum-2023",
          title: 'New conference paper accepted in Forum Acusticum 2023!',
          description: "",
          section: "News",},{id: "news-new-book-chapter-published",
          title: 'New Book chapter published!',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2024-5-12.html";
            },},{id: "news-new-conference-paper-in-the-asa-2024",
          title: 'New conference paper in the ASA 2024!',
          description: "",
          section: "News",},{id: "news-new-paper-out-in-the-journal-of-exposure-science-amp-environmental-epidemiology",
          title: 'New paper out in the Journal of Exposure Science &amp;amp; Environmental Epidemiology',
          description: "",
          section: "News",handler: () => {
              window.location.href = "/news/2024-6-12.html";
            },},{id: "news-prof-méndez-echenagucia-promoted-to-associate-professor",
          title: 'Prof. Méndez Echenagucia promoted to Associate Professor',
          description: "",
          section: "News",},{id: "projects-hilo-unit",
          title: 'HiLo Unit',
          description: "Experimental office space in the EMPA campus, Switzerland.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project.html";
            },},{id: "projects-eth-pavillion",
          title: 'ETH Pavillion',
          description: "Pavillion for the Ideas City Festival in New York City.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/2_project.html";
            },},{id: "projects-hilo-roof-prototype",
          title: 'Hilo Roof Prototype',
          description: "Real-scale test of the cable-net and fabric formwork",
          section: "Projects",handler: () => {
              window.location.href = "/projects/3_project.html";
            },},{id: "projects-beyond-bending",
          title: 'Beyond Bending',
          description: "Exhibition at the Venice Biennale.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/4_project.html";
            },},{id: "projects-droneport-prototype",
          title: 'Droneport Prototype',
          description: "Exhibition at the Venice Biennale.",
          section: "Projects",handler: () => {
              window.location.href = "/projects/5_project.html";
            },},{id: "projects-mycotree",
          title: 'MycoTree',
          description: "Exhibition at the Seoul Biennale 2017",
          section: "Projects",handler: () => {
              window.location.href = "/projects/6_project.html";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%74%6D%65%6E%64%65%7A%65@%75%77.%65%64%75", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/tmsmendez", "_blank");
        },
      },{
        id: 'social-scholar',
        title: 'Google Scholar',
        section: 'Socials',
        handler: () => {
          window.open("https://scholar.google.com/citations?user=OyDWXZwAAAAJ", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
