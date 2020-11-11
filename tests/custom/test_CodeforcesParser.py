from oiTerminal.custom.Codeforces.CodeforcesParser import CodeforcesParser
from oiTerminal.model.ParseProblemResult import ParseProblemResult
from oiTerminal.utils.HtmlTag import HtmlTag
from oiTerminal.utils.HttpUtil import HttpUtil
from oiTerminal.utils.Logger import getLogger


def test_codeforces_parser():
    test_doc: str = r"""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html lang="en">
<head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
    <meta name="X-Csrf-Token" content="5c7447a4c7e1ed4a7bde649a69110c7c"/>
    <meta id="viewport" name="viewport" content="width=device-width, initial-scale=0.01"/>

    <!-- Google Tag Manager -->
    <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
            j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
            'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
        })(window,document,'script','dataLayer','GTM-5P98');</script>
    <!-- End Google Tag Manager -->

    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery-1.8.3.js"></script>
    <script type="application/javascript">
        window.standaloneContest = false;
        function adjustViewport() {
            var screenWidthPx = Math.min($(window).width(), window.screen.width);
            var siteWidthPx = 1100; // min width of site
            var ratio = Math.min(screenWidthPx / siteWidthPx, 1.0);
            var viewport = "width=device-width, initial-scale=" + ratio;
            $('#viewport').attr('content', viewport);
            var style = $('<style>html * { max-height: 1000000px; }</style>');
            $('html > head').append(style);
        }

        if ( /Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(navigator.userAgent) ) {
            adjustViewport();
        }

        /* Protection against trailing dot in domain. */
        let hostLength = window.location.host.length;
        if (hostLength > 1 && window.location.host[hostLength - 1] === '.') {
            window.location = window.location.protocol + "//" + window.location.host.substring(0, hostLength - 1);
        }
    </script>
    <meta http-equiv="pragma" content="no-cache">
    <meta http-equiv="expires" content="-1">
    <meta http-equiv="profileName" content="h2">
    <meta name="google-site-verification" content="OTd2dN5x4nS4OPknPI9JFg36fKxjqY0i1PSfFPv_J90"/>
    <meta property="fb:admins" content="100001352546622" />
    <meta property="og:image" content="//sta.codeforces.com/s/63895/images/codeforces-telegram-square.png" />
    <link rel="image_src" href="//sta.codeforces.com/s/63895/images/codeforces-telegram-square.png" />
    <meta property="og:title" content="Problem - A - Codeforces"/>
    <meta property="og:description" content=""/>
    
    <meta property="og:site_name" content="Codeforces"/>
    
    
    
    <meta name="cc" content="1808b649c6f374622cd00885dbce88dafdee4aa9"/>
    
    
    <meta name="utc_offset" content="+03:00"/>
    <meta name="verify-reformal" content="f56f99fd7e087fb6ccb48ef2" />
    <title>Problem - A - Codeforces</title>
        <meta name="description" content="Codeforces. Programming competitions and contests, programming community" />
        <meta name="keywords" content="programming algorithm contest competition informatics olympiads c++ java graphs vkcup" />
    <meta name="robots" content="index, follow" />

    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/font-awesome.min.css" type="text/css" charset="utf-8" />

        <link href='//fonts.googleapis.com/css?family=PT+Sans+Narrow:400,700&subset=latin,cyrillic' rel='stylesheet' type='text/css'>
        <link href='//fonts.googleapis.com/css?family=Cuprum&subset=latin,cyrillic' rel='stylesheet' type='text/css'>


    <link rel="apple-touch-icon" sizes="57x57" href="//sta.codeforces.com/s/63895/apple-icon-57x57.png">
    <link rel="apple-touch-icon" sizes="60x60" href="//sta.codeforces.com/s/63895/apple-icon-60x60.png">
    <link rel="apple-touch-icon" sizes="72x72" href="//sta.codeforces.com/s/63895/apple-icon-72x72.png">
    <link rel="apple-touch-icon" sizes="76x76" href="//sta.codeforces.com/s/63895/apple-icon-76x76.png">
    <link rel="apple-touch-icon" sizes="114x114" href="//sta.codeforces.com/s/63895/apple-icon-114x114.png">
    <link rel="apple-touch-icon" sizes="120x120" href="//sta.codeforces.com/s/63895/apple-icon-120x120.png">
    <link rel="apple-touch-icon" sizes="144x144" href="//sta.codeforces.com/s/63895/apple-icon-144x144.png">
    <link rel="apple-touch-icon" sizes="152x152" href="//sta.codeforces.com/s/63895/apple-icon-152x152.png">
    <link rel="apple-touch-icon" sizes="180x180" href="//sta.codeforces.com/s/63895/apple-icon-180x180.png">
    <link rel="icon" type="image/png" sizes="192x192"  href="//sta.codeforces.com/s/63895/android-icon-192x192.png">
    <link rel="icon" type="image/png" sizes="32x32" href="//sta.codeforces.com/s/63895/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="96x96" href="//sta.codeforces.com/s/63895/favicon-96x96.png">
    <link rel="icon" type="image/png" sizes="16x16" href="//sta.codeforces.com/s/63895/favicon-16x16.png">
    <link rel="manifest" href="//sta.codeforces.com/s/63895/manifest.json">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="msapplication-TileImage" content="//sta.codeforces.com/s/63895/ms-icon-144x144.png">
    <meta name="theme-color" content="#ffffff">

    <!--CombineResourcesFilter-->
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/prettify.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/clear.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/style.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/ttypography.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/problem-statement.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/second-level-menu.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/roundbox.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/datatable.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/table-form.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/topic.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/jquery.jgrowl.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/facebox.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/jquery.wysiwyg.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/jquery.autocomplete.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/codeforces.datepick.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/colorbox.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/jquery.drafts.css" type="text/css" charset="utf-8" />
        <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/community.css" type="text/css" charset="utf-8" />
        <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/status.css" type="text/css" charset="utf-8" />
        <link rel="stylesheet" href="//sta.codeforces.com/s/63895/css/sidebar-menu.css" type="text/css" charset="utf-8" />

    <!-- MathJax -->
    <script type="text/x-mathjax-config">
    MathJax.Hub.Config({
      tex2jax: {inlineMath: [['$$$','$$$']], displayMath: [['$$$$$$','$$$$$$']]}
    });
    MathJax.Hub.Register.StartupHook("End", function () {
        Codeforces.runMathJaxListeners();
    });
    </script>
    <script type="text/javascript" async
            src="https://assets.codeforces.com/mathjax/MathJax.js?config=TeX-AMS_HTML-full"
    >
    </script>
    <!-- /MathJax -->

    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/prettify/prettify.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/moment-with-locales.min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/pushstream.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.easing.min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.lavalamp.min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.jgrowl.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.swipe.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.hotkeys.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/facebox.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.wysiwyg.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/controls/wysiwyg.colorpicker.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/controls/wysiwyg.table.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/controls/wysiwyg.image.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/controls/wysiwyg.link.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.autocomplete.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/ua-parser.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.datepick.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.ie6blocker.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.colorbox-min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.ba-bbq.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/jquery.drafts.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/clipboard.min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/autosize.min.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/sjcl.js"></script>
    <script type="text/javascript" src="/scripts/51118cd65ac5d676d07b6d1851ce48c3/en/codeforces-options.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/codeforces.js?v=20160131"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/EventCatcher.js?v=20160131"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/js/preparedVerdictFormats-en.js"></script>
    <!--/CombineResourcesFilter-->

    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/markitup/skins/markitup/style.css" type="text/css" charset="utf-8" />
    <link rel="stylesheet" href="//sta.codeforces.com/s/63895/markitup/sets/markdown/style.css" type="text/css" charset="utf-8" />


    <script type="text/javascript" src="//sta.codeforces.com/s/63895/markitup/jquery.markitup.js"></script>
    <script type="text/javascript" src="//sta.codeforces.com/s/63895/markitup/sets/markdown/set.js"></script>

    <!--[if IE]>
    <style>
        #sidebar {
            padding-left: 1em;
            margin: 1em 1em 1em 0;
        }
    </style>
    <![endif]-->



</head>
<body class=" "><span style='display:none;' class='csrf-token' data-csrf='5c7447a4c7e1ed4a7bde649a69110c7c'>&nbsp;</span>
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-5P98"
                  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->

<!-- .notificationTextCleaner used in Codeforces.showAnnouncements() -->
<div class="notificationTextCleaner" style="font-size: 0px"></div>
<div class="button-up" style="display: none; opacity: 0.7; width: 50px; height:100%; position: fixed; left: 0; top: 0; cursor: pointer; text-align: center; line-height: 35px; color: #d3dbe4; font-weight: bold; font-size: 3.0rem;"><i class="icon-circle-arrow-up"></i></div>
<div class="verdictPrototypeDiv" style="display: none;"></div>

<!-- Codeforces JavaScripts. -->
<script type="text/javascript">
    String.prototype.hashCode = function() {
        var hash = 0, i, chr;
        if (this.length === 0) return hash;
        for (i = 0; i < this.length; i++) {
            chr   = this.charCodeAt(i);
            hash  = ((hash << 5) - hash) + chr;
            hash |= 0; // Convert to 32bit integer
        }
        return hash;
    };

    var queryMobile = Codeforces.queryString.mobile;
    if (queryMobile === "true" || queryMobile === "false") {
        Codeforces.putToStorage("useMobile", queryMobile == "true");
    } else {
        var useMobile = Codeforces.getFromStorage("useMobile");
        if (useMobile === true || useMobile === false) {
            if (useMobile != false) {
                Codeforces.redirect(Codeforces.updateUrlParameter(document.location.href, "mobile", useMobile));
            }
        }
    }
</script>

<script type="text/javascript">
    if (window.parent.frames.length > 0) {
        window.stop();
    }
</script>



<script type="text/javascript">
    window.fbAsyncInit = function() {
        FB.init({
            appId      : '554666954583323',
            xfbml      : true,
            version    : 'v2.8'
        });
        FB.AppEvents.logPageView();
    };

    (function(d, s, id){
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) {return;}
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/en_US/sdk.js";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));
</script>


    <script type="text/javascript">
        $(document).ready(function () {
    (function () {
        jQuery.expr[':'].containsCI = function(elem, index, match) {
            return !match || !match.length || match.length < 4 || !match[3] || (
                    elem.textContent || elem.innerText || jQuery(elem).text() || ''
            ).toLowerCase().indexOf(match[3].toLowerCase()) >= 0;
        }
    }(jQuery));

    $.ajaxPrefilter(function(options, originalOptions, xhr) {
        var csrf = Codeforces.getCsrfToken();

        if (csrf) {
            var data = originalOptions.data;
            if (originalOptions.data !== undefined) {
                if (Object.prototype.toString.call(originalOptions.data) === '[object String]') {
                    data = $.deparam(originalOptions.data);
                }
            } else {
                data = {};
            }
            options.data = $.param($.extend(data, { csrf_token: csrf }));
        }
    });

    window.getCodeforcesServerTime = function(callback) {
        $.post("/data/time", {}, callback, "json");
    }

    window.updateTypography = function () {
        $("div.ttypography code").addClass("tt");
        $("div.ttypography pre>code").addClass("prettyprint").removeClass("tt");
        $("div.ttypography table").addClass("bordertable");
        prettyPrint();
    }

    $.ajaxSetup({ scriptCharset: "utf-8" ,contentType: "application/x-www-form-urlencoded; charset=UTF-8", headers: {
        'X-Csrf-Token': Codeforces.getCsrfToken()
    }});

    window.updateTypography();

    Codeforces.signForms();

    setTimeout(function() {
        $(".second-level-menu-list").lavaLamp({
            fx: "backout",
            speed: 700
        });
    }, 100);


    Codeforces.countdown();
    $("a[rel='photobox']").colorbox();


    function showAnnouncements(json) {
        //info("j=" + JSON.stringify(json));

        if (json.t != "a") {
            return;
        }

        setTimeout(function() {
            Codeforces.showAnnouncements(json.d, "en");
        }, Math.random() * 500);
    }

    function showEventCatcherUserMessage(json) {
        if (json.t == "s") {
            var points = json.d[5];
            var passedTestCount = json.d[7];
            var judgedTestCount = json.d[8];
            var verdict = preparedVerdictFormats[json.d[12]];
            var verdictPrototypeDiv = $(".verdictPrototypeDiv");
            verdictPrototypeDiv.html(verdict);
            if (judgedTestCount != null && judgedTestCount != undefined) {
                verdictPrototypeDiv.find(".verdict-format-judged").text(judgedTestCount);
            }
            if (passedTestCount != null && passedTestCount != undefined) {
                verdictPrototypeDiv.find(".verdict-format-passed").text(passedTestCount);
            }
            if (points != null && points != undefined) {
                verdictPrototypeDiv.find(".verdict-format-points").text(points);
            }
            Codeforces.showMessage(verdictPrototypeDiv.text());
        }
    }

    $(".clickable-title").each(function() {
        var title = $(this).attr("data-title");
        if (title) {
            var tmp = document.createElement("DIV");
            tmp.innerHTML = title;
            $(this).attr("title", tmp.textContent || tmp.innerText || "");
        }
    });

    $(".clickable-title").click(function() {
        var title = $(this).attr("data-title");
        if (title) {
            Codeforces.alert(title);
        } else {
            Codeforces.alert($(this).attr("title"));
        }
    }).css("position", "relative").css("bottom", "3px");

        Codeforces.showDelayedMessage();

    Codeforces.reformatTimes();

    //Codeforces.initializePubSub();
    if (window.codeforcesOptions.subscribeServerUrl) {
        window.eventCatcher = new EventCatcher(
            window.codeforcesOptions.subscribeServerUrl,
            [
                Codeforces.getGlobalChannel(),
                Codeforces.getUserChannel(),
                Codeforces.getUserShowMessageChannel(),
                Codeforces.getContestChannel(),
                Codeforces.getParticipantChannel(),
                Codeforces.getTalkChannel()
            ]
        );

        if (Codeforces.getParticipantChannel()) {
            window.eventCatcher.subscribe(Codeforces.getParticipantChannel(), function(json) {
                showAnnouncements(json);
            });
        }

        if (Codeforces.getContestChannel()) {
            window.eventCatcher.subscribe(Codeforces.getContestChannel(), function(json) {
                showAnnouncements(json);
            });
        }

        if (Codeforces.getGlobalChannel()) {
            window.eventCatcher.subscribe(Codeforces.getGlobalChannel(), function(json) {
                showAnnouncements(json);
            });
        }

        if (Codeforces.getUserChannel()) {
            window.eventCatcher.subscribe(Codeforces.getUserChannel(), function(json) {
                showAnnouncements(json);
            });
        }

        if (Codeforces.getUserShowMessageChannel()) {
            window.eventCatcher.subscribe(Codeforces.getUserShowMessageChannel(), function(json) {
                showEventCatcherUserMessage(json);
            });
        }
    }

    Codeforces.setupContestTimes("/data/contests");
    Codeforces.setupSpoilers();
    Codeforces.setupTutorials("/data/problemTutorial");
        });
    </script>

<script type="text/javascript">
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-743380-5']);
  _gaq.push(['_trackPageview']);

  (function () {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = (document.location.protocol == 'https:' ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>


<div id="body">
        

<div class="side-bell" style="visibility: hidden; display: none; opacity: 0.7; width: 40px; position: fixed; right: 0; top: 0; cursor: pointer; text-align: center; line-height: 35px; color: #d3dbe4; font-weight: bold; font-size: 1.5rem;">
    <span class="icon-stack" style="width: 100%;">
        <i class="icon-circle icon-stack-base"></i>
        <i class="icon-bell-alt icon-light"></i>
    </span>
    <br/>
    <span class="side-bell__count" style="position: relative; top: -10px;"></span>
</div>


<div id="header" style="position: relative;">
    <div style="float:left;">
            <div><a href="/kotlin"><img style="position:relative;top:4px;" src="//assets.codeforces.com/images/kh/kotlin_heroes_page_header-55.png"/></a></div>

    </div>
    <div class="lang-chooser">
        <div style="text-align: right;">
            <a href="?locale=en"><img src="//sta.codeforces.com/s/63895/images/flags/24/gb.png" title="In English" alt="In English"/></a>
            <a href="?locale=ru"><img src="//sta.codeforces.com/s/63895/images/flags/24/ru.png" title="По-русски" alt="По-русски"/></a>
        </div>

        <div >
                        <a href="/enter?back=%2Fcontest%2F1432%2Fproblem%2FA">Enter</a>
                     | 
                        <a href="/register">Register</a>
                    
        </div>



    </div>
    <br style="clear: both;"/>
</div>
        

    <div class="roundbox menu-box" style="">
            <div class="roundbox-lt">&nbsp;</div>
            <div class="roundbox-rt">&nbsp;</div>
            <div class="roundbox-lb">&nbsp;</div>
            <div class="roundbox-rb">&nbsp;</div>
    <div class="menu-list-container">
    <ul class="menu-list main-menu-list">
                <li class=""><a href="/">Home</a></li>
                <li class=""><a href="/top">Top</a></li>
                <li class="current"><a href="/contests">Contests</a></li>
                <li class=""><a href="/gyms">Gym</a></li>
                <li class=""><a href="/problemset">Problemset</a></li>
                <li class=""><a href="/groups">Groups</a></li>
                <li class=""><a href="/ratings">Rating</a></li>
                <li class=""><a href="/edu/courses"><span class="edu-menu-item">Edu</span></a></li>
                <li class=""><a href="/apiHelp">API</a></li>
                <li class=""><a href="/calendar">Calendar</a></li>
                <li class=""><a href="/help">Help</a></li>
                <li class=""><a href="/10years"><span style="color:#ce2a2a;font-weight:bold;">10 years! <i style="font-size:100%" class="icon-gift"></i></span></a></li>
    </ul>
        <form method="post" action="/search"><input type='hidden' name='csrf_token' value='5c7447a4c7e1ed4a7bde649a69110c7c'/>
            <input class="search" name="query" data-isPlaceholder="true" value=""/>
        </form>
    <br style="clear: both;"/>
</div>

    </div>

    <script type="text/javascript">
        $(document).ready(function () {
            $("input.search").focus(function () {
                if ($(this).attr("data-isPlaceholder") === "true") {
                    $(this).val("");
                    $(this).removeAttr("data-isPlaceholder");
                }
            });
        });
    </script>
            <br style="height: 3em; clear: both;"/>

        <div style="position: relative;">
                        <div id="sidebar">

    <div class="roundbox sidebox" style="">
            <div class="roundbox-lt">&nbsp;</div>
            <div class="roundbox-rt">&nbsp;</div>
        <table class="rtable ">
            <tbody>
                <tr>
                            <th class="left" style="width:100%;"><a style="color: black" href="/contest/1432">Kotlin Heroes 5: ICPC Round (Practice)</a></th>
                </tr>
                    <tr>
                                <td class="left  dark" colspan="1"><span class="contest-state-phase">Contest is running</span></td>
                    </tr>
                    <tr>
                                <td class="left bottom" colspan="1"><span class='contest-state-regular countdown before-contest-1432-finish' home='//sta.codeforces.com/s/63895' noRedirection='true' textBeforeRedirect='The coding phase of "Kotlin Heroes 5: ICPC Round (Practice)" is finished, reload the page to view changes'><span title="59:26:49">2 days</span></span></td>
                    </tr>
            </tbody>
        </table>
    </div>

    <div class="roundbox sidebox" style="">
            <div class="roundbox-lt">&nbsp;</div>
            <div class="roundbox-rt">&nbsp;</div>
        <div class="caption titled">&rarr; Languages
            <div class="top-links">
            </div>
        </div>
<div style="margin:1em;">
    <div style="font-size:0.8em;">The following languages are only available languages for the problems from the contest</div><div style="font-weight:bold;margin:0.5em 0;font-size:0.8em;text-align:center;">Kotlin Heroes 5: ICPC Round (Practice):</div>
<ul class="list" style="font-size:0.8em;margin-top:0.5em;">
        <li>Kotlin 1.4.0</li>
</ul>
</div>
    </div>


</div>
                        <div id="pageContent" class="content-with-sidebar">
                    <div class="second-level-menu">
<ul class="second-level-menu-list">
        <li class="current selectedLava"><a
                                        href="/contest/1432">Problems</a></li>
        <li><a
                                        href="/contest/1432/submit">Submit Code</a></li>
        <li><a
                                        href="/contest/1432/my">My Submissions</a></li>
        <li><a
                                        href="/contest/1432/status">Status</a></li>
        <li><a
                                        href="/contest/1432/standings">Standings</a></li>
        <li><a
                                        href="/contest/1432/customtest">Custom Invocation</a></li>
</ul>
</div>

    <style>
        #facebox .content:has(.diff-popup) {
            width: 90vw;
            max-width: 120rem !important;
        }

        .diff-popup {
            width: 90vw;
            max-width: 120rem !important;
            display: none;
            overflow: auto;
        }

        .input-output-copier {
            font-size: 1.2rem;
            float: right;
            color: #888 !important;
            cursor: pointer;
            border: 1px solid rgb(185, 185, 185);
            padding: 3px;
            margin: 1px;
            line-height: 1.1rem;
            text-transform: none;
        }

        .input-output-copier:hover {
            background-color: #def;
        }

        .test-explanation textarea {
            width: 100%;
            height: 1.5em;
        }

        .pending-submission-message {
            color: darkorange !important;
        }
    </style>
    <script>
        const OPENING_SPACE = String.fromCharCode(1001);
        const CLOSING_SPACE = String.fromCharCode(1002);

        const nodeToText = function (node, pre) {
            let result = [];

            if (node.tagName === "SCRIPT" || node.tagName === "math"
                || (node.classList && node.classList.contains("input-output-copier")))
                return [];

            if (node.tagName === "NOBR") {
                result.push(OPENING_SPACE);
            }

            if (node.nodeType === Node.TEXT_NODE) {
                let s = node.textContent;
                if (!pre) {
                    s = s.replace(/\s+/g, " ");
                }
                if (s.length > 0) {
                    result.push(s);
                }
            }

            if (pre && node.tagName === "BR") {
                result.push("\n");
            }

            node.childNodes.forEach(function (child) {
                result.push(nodeToText(child, node.tagName === "PRE").join(""));
            });

            if (node.tagName === "DIV"
                || node.tagName === "P"
                || node.tagName === "PRE"
                || node.tagName === "UL"
                || node.tagName === "LI"
            ) {
                result.push("\n");
            }

            if (node.tagName === "NOBR") {
                result.push(CLOSING_SPACE);
            }

            return result;
        }

        const isSpecial = function (c) {
            return c === ',' || c === '.' || c === ';' || c === ')' || c === ' ';
        }

        const convertStatementToText = function(statmentNode) {
            const text = nodeToText(statmentNode, false).join("").replace(/ +/g, " ").replace(/\n\n+/g, "\n\n");
            let result = [];
            for (let i = 0; i < text.length; i++) {
                const c = text.charAt(i);
                if (c === OPENING_SPACE) {
                    if (!((i > 0 && text.charAt(i - 1) === '(') || (result.length > 0 && result[result.length - 1] === ' '))) {
                        result.push('+');
                    }
                } else if (c === CLOSING_SPACE) {
                    if (!(i + 1 < text.length && isSpecial(text.charAt(i + 1)))) {
                        result.push('-');
                    }
                } else {
                    result.push(c);
                }
            }
            return result.join("").split("\n").map(value => value.trim()).join("\n");
        };
    </script>
    <div class="diff-popup">
    </div>

<div class="problemindexholder" problemindex="A" data-uuid="ps_406c72572319fa7fb467e579c3d28683d8201689">
    <div style="display: none; margin:1em 0;text-align: center; position: relative;" class="alert alert-info diff-notifier">
        <div>The problem statement has recently been changed. <a class="view-changes" href="#">View the changes.</a></div>
        <span class="diff-notifier-close" style="position: absolute; top: 0.2em; right: 0.3em; cursor: pointer; font-size: 1.4em;">&times;</span>
    </div>
        <div class="ttypography"><div class="problem-statement"><div class="header"><div class="title">A. A+B (Trial Problem)</div><div class="time-limit"><div class="property-title">time limit per test</div>2.0 s</div><div class="memory-limit"><div class="property-title">memory limit per test</div>512 MB</div><div class="input-file"><div class="property-title">input</div>standard input</div><div class="output-file"><div class="property-title">output</div>standard output</div></div><div><p>You are given two integers $$$a$$$ and $$$b$$$. Print $$$a+b$$$.</p></div><div class="input-specification"><div class="section-title">Input</div><p>The first line contains an integer $$$t$$$ ($$$1 \le t \le 10^4$$$) — the number of test cases in the input. Then $$$t$$$ test cases follow.</p><p>Each test case is given as a line of two integers $$$a$$$ and $$$b$$$ ($$$-1000 \le a, b \le 1000$$$).</p></div><div class="output-specification"><div class="section-title">Output</div><p>Print $$$t$$$ integers — the required numbers $$$a+b$$$.</p></div><div class="sample-tests"><div class="section-title">Example</div><div class="sample-test"><div class="input"><div class="title">Input</div><pre>
4
1 5
314 15
-99 99
123 987
</pre></div><div class="output"><div class="title">Output</div><pre>
6
329
0
1110
</pre></div></div></div></div><p>  </p></div>
</div>

    <script>
        $(function () {
            Codeforces.addMathJaxListener(function () {
                let $problem = $("div[problemindex=A]");
                let uuid = $problem.attr("data-uuid");
                let statementText = convertStatementToText($problem.find(".ttypography").get(0));

                let previousStatementText = Codeforces.getFromStorage(uuid);
                if (previousStatementText) {
                    if (previousStatementText !== statementText) {
                        $problem.find(".diff-notifier").show();

                        $problem.find(".diff-notifier-close").click(function() {
                            Codeforces.putToStorageTtl(uuid, statementText, 6 * 60 * 60);
                            $problem.find(".diff-notifier").hide();
                        });

                        $problem.find("a.view-changes").click(function() {
                            $.post("/data/diff", {action: "getDiff", a: previousStatementText, b: statementText}, function (result) {
                                if (result["success"] === "true") {
                                    Codeforces.facebox(".diff-popup", "//sta.codeforces.com/s/63895");
                                    $("#facebox .diff-popup").html(result["diff"]);
                                }
                            }, "json");
                        });
                    }
                } else {
                    Codeforces.putToStorageTtl(uuid, statementText, 6 * 60 * 60);
                }
            });
        });
    </script>


<script type="text/javascript">
    $(document).ready(function () {
        window.changedTests = new Set();
        console.log("Initialized window.changedTests.");

        function endsWith(string, suffix) {
            return string.indexOf(suffix, string.length - suffix.length) !== -1;
        }

        var inputFileDiv = $("div.input-file");
        var inputFile = inputFileDiv.text();
        var outputFileDiv = $("div.output-file");
        var outputFile = outputFileDiv.text();


        if (!endsWith(inputFile, "standard input")
            && !endsWith(inputFile, "standard input")) {
            inputFileDiv.attr("style", "font-weight: bold");
        }

        if (!endsWith(outputFile, "standard output")
            && !endsWith(outputFile, "standard output")) {
            outputFileDiv.attr("style", "font-weight: bold");
        }

        var titleDiv = $("div.header div.title");



        String.prototype.replaceAll = function (search, replace) {
            return this.split(search).join(replace);
        };

        $(".sample-test .title").each(function () {
            var preId = ("id" + Math.random()).replaceAll(".", "0");
            var cpyId = ("id" + Math.random()).replaceAll(".", "0");

            $(this).parent().find("pre").attr("id", preId);
            var $copy = $("<div title='Copy' data-clipboard-target='#" + preId + "' id='" + cpyId + "' class='input-output-copier'>Copy</div>");
            $(this).append($copy);

            var clipboard = new Clipboard('#' + cpyId, {
                text: function (trigger) {
                    return Codeforces.filterClipboardText(document.querySelector('#' + preId).innerText);
                }
            });

            var isInput = $(this).parent().hasClass("input");

            clipboard.on('success', function (e) {
                if (isInput) {
                    Codeforces.showMessage("The example input has been copied into the clipboard");
                } else {
                    Codeforces.showMessage("The example output has been copied into the clipboard");
                }
                e.clearSelection();
            });
        });

        $(".test-form-item input").change(function () {
            addPendingSubmissionMessage($($(this).closest("form")), "You changed the answer, do not forget to submit it if you want to save the changes");
            var index = $(this).closest(".problemindexholder").attr("problemindex");
            var test = "";
            $(this).closest("form input").each(function () {
                var test_ = $(this).attr("name");
                if (test_ && test_.substring(0, 4) === "test") {
                    test = test_;
                }
            });
            if (index.length > 0 && test.length > 0) {
                var indexTest = index + "::" + test;
                window.changedTests.add(indexTest);
            }
        });

        $(window).on('beforeunload', function () {
            if (window.changedTests.size > 0) {
                return 'Dialog text here';
            }
        });

        autosize($('.test-explanation textarea'));

    });
</script>

                </div>
        </div>
            <br style="clear: both;"/>
            <div id="footer">
                <div><a href="https://codeforces.com/">Codeforces</a> (c) Copyright 2010-2020 Mike Mirzayanov</div>
                <div>The only programming contests Web 2.0 platform</div>
                    <div>Server time: <span class="format-timewithseconds" data-locale="en">Nov/10/2020 05:08:11</span> (h2).</div>
                    <div>Desktop version, switch to <a rel="nofollow" class="switchToMobile" href="?mobile=true">mobile version</a>.</div>
                <div class="smaller"><a href="/privacy">Privacy Policy</a></div>

                    <div style="margin-top: 25px;">
                        Supported by
                    </div>
                    <div style="margin-top: 8px; padding-bottom: 20px; position: relative; left: 10px;">
                        <a href="https://telegram.org/"><img style="margin-right: 2em; width: 60px;" src="//sta.codeforces.com/s/63895/images/telegram-100x100.png" alt="Telegram" title="Telegram"/></a>
                        <a href="http://ifmo.ru/en/"><img style="width: 120px;" src="//sta.codeforces.com/s/63895/images/itmo_small_en-logo.png" alt="ИТМО" title="ИТМО"/></a>
                    </div>
            </div>
        <script type="text/javascript">
            $(function() {
                $(".switchToMobile").click(function() {
                    Codeforces.redirect(Codeforces.updateUrlParameter(document.location.href, "mobile", "true"));
                    return false;
                });
                $(".switchToDesktop").click(function() {
                    Codeforces.redirect(Codeforces.updateUrlParameter(document.location.href, "mobile", "false"));
                    return false;
                });
            });
        </script>
    <script type="text/javascript">
        $(document).ready(function () {
            if ($(window).width() < 1600) {
                $('.button-up').css('width', '30px').css('line-height', '30px').css('font-size', '20px');
            }

            if ($(window).width() >= 1200) {
                $ (window).scroll (function () {
                    if ($ (this).scrollTop () > 100) {
                        $ ('.button-up').fadeIn();
                    } else {
                        $ ('.button-up').fadeOut();
                    }
                });

                $('.button-up').click(function () {
                    $('body,html').animate({
                        scrollTop: 0
                    }, 500);
                    return false;
                });

                $('.button-up').hover(function () {
                    $(this).animate({
                        'opacity':'1'
                    }).css({'background-color':'#e7ebf0','color':'#6a86a4'});
                }, function () {
                    $(this).animate({
                        'opacity':'0.7'
                    }).css({'background':'none','color':'#d3dbe4'});;
                });
            }
            Codeforces.focusOnError();
        });
    </script>

        <div class="userListsFacebox" style="display:none;">
            <div style="padding: 0.5em; width: 600px; max-height: 200px; overflow-y: auto">
<div class="datatable"
     
     style="background-color: #E1E1E1; padding-bottom: 3px;">
            <div class="lt">&nbsp;</div>
            <div class="rt">&nbsp;</div>
            <div class="lb">&nbsp;</div>
            <div class="rb">&nbsp;</div>

            <div style="padding: 4px 0 0 6px;font-size:1.4rem;position:relative;">
                User lists

                <div style="position:absolute;right:0.25em;top:0.35em;">
                    <span style="padding:0;position:relative;bottom:2px;" class="rowCount"></span>

                    <img class="closed" src="//sta.codeforces.com/s/63895/images/icons/control.png"/>

                    <span class="filter" style="display:none;">
                        <img class="opened" src="//sta.codeforces.com/s/63895/images/icons/control-270.png"/>
                        <input style="padding:0 0 0 20px;position:relative;bottom:2px;border:1px solid #aaa;height:17px;font-size:1.3rem;"/>
                    </span>
                </div>
            </div>
            <div style="background-color: white;margin:0.3em 3px 0 3px;position:relative;">
            <div class="ilt">&nbsp;</div>
            <div class="irt">&nbsp;</div>
            <table class="">
                    <thead>
                    <tr>
                        <th>Name</th>
                    </tr>
                    </thead>
                    <tbody>
                    </tbody>
            </table>
            </div>
        </div>
    <script type="text/javascript">
        $(document).ready(function () {
                // Create new ':containsIgnoreCase' selector for search
                jQuery.expr[':'].containsIgnoreCase = function(a, i, m) {
                    return jQuery(a).text().toUpperCase()
                            .indexOf(m[3].toUpperCase()) >= 0;
                };

                if (window.updateDatatableFilter == undefined) {
                    window.updateDatatableFilter = function(i) {
                        var parent = $(i).parent().parent().parent().parent();
                        $("tr.no-items", parent).remove();
                        $("tr", parent).hide().removeClass('visible');
                        var text = $(i).val();
                        if (text) {
                            $("tr" + ":containsIgnoreCase('" + text + "')", parent).show().addClass('visible');
                        } else {
                            parent.find(".rowCount").text("");
                            $("tr", parent).show().addClass('visible');
                        }

                        var found = false;
                        var visibleRowCount = 0;
                        $("tr", parent).each(function () {
                            if (!found) {
                                if ($(this).find("th").size() > 0) {
                                    $(this).show().addClass('visible');
                                    found = true;
                                }
                            }
                            if ($(this).hasClass('visible')) {
                                visibleRowCount++;
                            }
                        });
                        if (text) {
                            parent.find(".rowCount").text("Matches: " + (visibleRowCount - (found ? 1 : 0)));
                        }
                        if (visibleRowCount == (found ? 1 : 0)) {
                            $("<tr class='no-items visible'><td style=\"text-align:left;\"colspan=\"32\">No items<\/td><\/tr>").appendTo($(parent).find('table'));
                        }
                        $(parent).find("tr td").removeClass("dark");
                        $(parent).find("tr.visible:odd td").addClass("dark");
                    }

                    $(".datatable .closed").click(function () {
                        var parent = $(this).parent();
                        $(this).hide();
                        $(".filter", parent).fadeIn(function () {
                            $("input", parent).val("").focus().css("border", "1px solid #aaa");
                        });
                    });

                    $(".datatable .opened").click(function () {
                        var parent = $(this).parent().parent();
                        $(".filter", parent).fadeOut(function () {
                            $(".closed", parent).show();
                            $("input", parent).val("").each(function () {
                                window.updateDatatableFilter(this);
                            });
                        });
                    });

                    $(".datatable .filter input").keyup(function(e) {
                        window.updateDatatableFilter(this);
                        e.preventDefault();
                        e.stopPropagation();
                    });

                    $(".datatable table").each(function () {
                        var found = false;
                        $("tr", this).each(function () {
                            if (!found && $(this).find("th").size() == 0) {
                                found = true;
                            }
                        });
                        if (!found) {
                            $("<tr class='no-items visible'><td style=\"text-align:left;\"colspan=\"32\">No items<\/td><\/tr>").appendTo(this);
                        }
                    });

                    // Applies styles to datatables.
                    $(".datatable").each(function () {
                        $(this).find("tr:first th").addClass("top");
                        $(this).find("tr:last td").addClass("bottom");
                        $(this).find("tr:odd td").addClass("dark");
                        $(this).find("tr td:first-child, tr th:first-child").addClass("left");
                        $(this).find("tr td:last-child, tr th:last-child").addClass("right");
                    });

                    $(".datatable table.tablesorter").each(function () {
                        $(this).bind("sortEnd", function () {
                            $(".datatable").each(function () {
                                $(this).find("th, td")
                                    .removeClass("top").removeClass("bottom")
                                    .removeClass("left").removeClass("right")
                                    .removeClass("dark");
                                $(this).find("tr:first th").addClass("top");
                                $(this).find("tr:last td").addClass("bottom");
                                $(this).find("tr:odd td").addClass("dark");
                                $(this).find("tr td:first-child, tr th:first-child").addClass("left");
                                $(this).find("tr td:last-child, tr th:last-child").addClass("right");
                            });
                        });
                    });
                }
        });
    </script>
            </div>
        </div>
        <script type="application/javascript">
            $(function() {
                $(".userListMarker").click(function() {
                    $.post("/data/lists", {action: "findTouched"}, function(json) {
                        Codeforces.facebox(".userListsFacebox");
                        var tbody = $("#facebox tbody");
                        tbody.empty();
                        for (var i in json) {
                            tbody.append(
                                    $("<tr></tr>").append(
                                            $("<td></td>").attr("data-readKey", json[i].readKey).text(json[i].name)
                                    )
                            );
                        }
                        Codeforces.updateDatatables();
                        tbody.find("td").css("cursor", "pointer").click(function() {
                            document.location = Codeforces.updateUrlParameter(document.location.href, "list", $(this).attr("data-readKey"));
                        });
                    }, "json");
                });
            });
        </script>
</div>
    <script type="application/javascript">
        if ('serviceWorker' in navigator && 'fetch' in window && 'caches' in window) {
            var parser = new UAParser();
            var browserName = parser.getBrowser().name;
            var browserVersion = parser.getBrowser().version;

            var supportedBrowser = false;
            var supportedBrowsers = {
                "Chrome": "76",
                "Firefox": "68",
                // "Edge": "18",
                "Safari": "12.1",
                "Opera": "63",
                "Yandex": "19.9"
            };

            for (var name in supportedBrowsers) {
                if (name === browserName && supportedBrowsers[name] <= browserVersion) {
                    supportedBrowser = true;
                }
            }

            if (supportedBrowser) {
                navigator.serviceWorker.register('/service-worker-63895.js')
                    .then(function (registration) {
                        console.log('Service worker registered');
                    })
                    .catch(function (error) {
                        console.log('Registration failed: ', error);
                    });
            } else {
                navigator.serviceWorker.getRegistrations().then(function(registrations) {
                    for (var i = 0; i < registrations.length; i++) {
                        registrations[i].unregister();
                    }
                });
            }
        }
    </script>
</body>
</html>
"""

    parser = CodeforcesParser(html_tag=HtmlTag(HttpUtil()), logger=getLogger('/tmp/oiTerminal/test.log'))
    parse_problem_result = parser.problem_parse(test_doc)
    assert parse_problem_result.status == ParseProblemResult.Status.NOTVIS
    assert parse_problem_result.title == 'A+B (Trial Problem)'
    assert parse_problem_result.test_cases[0].in_data == '4\n1 5\n314 15\n-99 99\n123 987'
    assert parse_problem_result.test_cases[0].out_data == '6\n329\n0\n1110'
    assert parse_problem_result.time_limit == '2.0 s'
    assert parse_problem_result.mem_limit == '512 MB'
