



<!DOCTYPE html>
<html lang="en" class=" is-copy-enabled">
  <head prefix="og: http://ogp.me/ns# fb: http://ogp.me/ns/fb# object: http://ogp.me/ns/object# article: http://ogp.me/ns/article# profile: http://ogp.me/ns/profile#">
    <meta charset='utf-8'>
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta http-equiv="Content-Language" content="en">
    <meta name="viewport" content="width=1020">
    
    
    <title>django-chunked-upload/README.rst at master · juliomalegria/django-chunked-upload</title>
    <link rel="search" type="application/opensearchdescription+xml" href="/opensearch.xml" title="GitHub">
    <link rel="fluid-icon" href="https://github.com/fluidicon.png" title="GitHub">
    <link rel="apple-touch-icon" sizes="57x57" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="114x114" href="/apple-touch-icon-114.png">
    <link rel="apple-touch-icon" sizes="72x72" href="/apple-touch-icon-144.png">
    <link rel="apple-touch-icon" sizes="144x144" href="/apple-touch-icon-144.png">
    <meta property="fb:app_id" content="1401488693436528">

      <meta content="@github" name="twitter:site" /><meta content="summary" name="twitter:card" /><meta content="juliomalegria/django-chunked-upload" name="twitter:title" /><meta content="django-chunked-upload - Upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted." name="twitter:description" /><meta content="https://avatars0.githubusercontent.com/u/1008637?v=3&amp;s=400" name="twitter:image:src" />
      <meta content="GitHub" property="og:site_name" /><meta content="object" property="og:type" /><meta content="https://avatars0.githubusercontent.com/u/1008637?v=3&amp;s=400" property="og:image" /><meta content="juliomalegria/django-chunked-upload" property="og:title" /><meta content="https://github.com/juliomalegria/django-chunked-upload" property="og:url" /><meta content="django-chunked-upload - Upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted." property="og:description" />
      <meta name="browser-stats-url" content="https://api.github.com/_private/browser/stats">
    <meta name="browser-errors-url" content="https://api.github.com/_private/browser/errors">
    <link rel="assets" href="https://assets-cdn.github.com/">
    <link rel="web-socket" href="wss://live.github.com/_sockets/NzE2NTQ3OTpmZDBiODZkYTdhOTEyNDU2ZjI2YzVhMjE4YTY3NWFjYTo2ZGU1MjE2MDcxNjExZDMyOGY4N2EzOGFmZTg3MjY0ZGI1MGM3MTRhMTA0Yjk3ZTdlMzE0ZTIxYjI1ZWJlMWVi--ee494e279f327b7e3a95d856b46a73e3607e509d">
    <meta name="pjax-timeout" content="1000">
    <link rel="sudo-modal" href="/sessions/sudo_modal">

    <meta name="msapplication-TileImage" content="/windows-tile.png">
    <meta name="msapplication-TileColor" content="#ffffff">
    <meta name="selected-link" value="repo_source" data-pjax-transient>

    <meta name="google-site-verification" content="KT5gs8h0wvaagLKAVWq8bbeNwnZZK1r1XQysX3xurLU">
    <meta name="google-analytics" content="UA-3769691-2">

<meta content="collector.githubapp.com" name="octolytics-host" /><meta content="github" name="octolytics-app-id" /><meta content="5FAF6819:6926:C8D04EC:566F4AB7" name="octolytics-dimension-request_id" /><meta content="7165479" name="octolytics-actor-id" /><meta content="Hannu1" name="octolytics-actor-login" /><meta content="37a6e0794dcc09b95ef5b467eaa45f896bf459ffdfcbb501779df99f8f0a267b" name="octolytics-actor-hash" />
<meta content="/&lt;user-name&gt;/&lt;repo-name&gt;/blob/show" data-pjax-transient="true" name="analytics-location" />
<meta content="Rails, view, blob#show" data-pjax-transient="true" name="analytics-event" />


  <meta class="js-ga-set" name="dimension1" content="Logged In">



        <meta name="hostname" content="github.com">
    <meta name="user-login" content="Hannu1">

        <meta name="expected-hostname" content="github.com">

      <link rel="mask-icon" href="https://assets-cdn.github.com/pinned-octocat.svg" color="#4078c0">
      <link rel="icon" type="image/x-icon" href="https://assets-cdn.github.com/favicon.ico">

    <meta content="c44ff91b7710a1e032987c1f3b1a1060710971b9" name="form-nonce" />

    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github-6c892d357361e0ff9ebc7541186e3ffc0e140cd8126f4a1793fab672476e857e.css" integrity="sha256-bIktNXNh4P+evHVBGG4//A4UDNgSb0oXk/q2ckduhX4=" media="all" rel="stylesheet" />
    <link crossorigin="anonymous" href="https://assets-cdn.github.com/assets/github2-97fc0640938a3d55d8aecab6168de6f96f99b4680728f1a2c03b794e6956e777.css" integrity="sha256-l/wGQJOKPVXYrsq2Fo3m+W+ZtGgHKPGiwDt5TmlW53c=" media="all" rel="stylesheet" />
    
    


    <meta http-equiv="x-pjax-version" content="4fe50be4c9729ffe76e44f9f68d62815">

      
  <meta name="description" content="django-chunked-upload - Upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted.">
  <meta name="go-import" content="github.com/juliomalegria/django-chunked-upload git https://github.com/juliomalegria/django-chunked-upload.git">

  <meta content="1008637" name="octolytics-dimension-user_id" /><meta content="juliomalegria" name="octolytics-dimension-user_login" /><meta content="11395627" name="octolytics-dimension-repository_id" /><meta content="juliomalegria/django-chunked-upload" name="octolytics-dimension-repository_nwo" /><meta content="true" name="octolytics-dimension-repository_public" /><meta content="false" name="octolytics-dimension-repository_is_fork" /><meta content="11395627" name="octolytics-dimension-repository_network_root_id" /><meta content="juliomalegria/django-chunked-upload" name="octolytics-dimension-repository_network_root_nwo" />
  <link href="https://github.com/juliomalegria/django-chunked-upload/commits/master.atom" rel="alternate" title="Recent Commits to django-chunked-upload:master" type="application/atom+xml">

  </head>


  <body class="logged_in   env-production windows vis-public page-blob">
    <a href="#start-of-content" tabindex="1" class="accessibility-aid js-skip-to-content">Skip to content</a>

    
    
    



      <div class="header header-logged-in true" role="banner">
  <div class="container clearfix">

    <a class="header-logo-invertocat" href="https://github.com/" data-hotkey="g d" aria-label="Homepage" data-ga-click="Header, go to dashboard, icon:logo">
  <span class="mega-octicon octicon-mark-github"></span>
</a>


      <div class="site-search repo-scope js-site-search" role="search">
          <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/juliomalegria/django-chunked-upload/search" class="js-site-search-form" data-global-search-url="/search" data-repo-search-url="/juliomalegria/django-chunked-upload/search" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
  <label class="js-chromeless-input-container form-control">
    <div class="scope-badge">This repository</div>
    <input type="text"
      class="js-site-search-focus js-site-search-field is-clearable chromeless-input"
      data-hotkey="s"
      name="q"
      placeholder="Search"
      aria-label="Search this repository"
      data-global-scope-placeholder="Search GitHub"
      data-repo-scope-placeholder="Search"
      tabindex="1"
      autocapitalize="off">
  </label>
</form>
      </div>

      <ul class="header-nav left" role="navigation">
        <li class="header-nav-item">
          <a href="/pulls" class="js-selected-navigation-item header-nav-link" data-ga-click="Header, click, Nav menu - item:pulls context:user" data-hotkey="g p" data-selected-links="/pulls /pulls/assigned /pulls/mentioned /pulls">
            Pull requests
</a>        </li>
        <li class="header-nav-item">
          <a href="/issues" class="js-selected-navigation-item header-nav-link" data-ga-click="Header, click, Nav menu - item:issues context:user" data-hotkey="g i" data-selected-links="/issues /issues/assigned /issues/mentioned /issues">
            Issues
</a>        </li>
          <li class="header-nav-item">
            <a class="header-nav-link" href="https://gist.github.com/" data-ga-click="Header, go to gist, text:gist">Gist</a>
          </li>
      </ul>

    
<ul class="header-nav user-nav right" id="user-links">
  <li class="header-nav-item">
      <span class="js-socket-channel js-updatable-content"
        data-channel="notification-changed:Hannu1"
        data-url="/notifications/header">
      <a href="/notifications" aria-label="You have no unread notifications" class="header-nav-link notification-indicator tooltipped tooltipped-s" data-ga-click="Header, go to notifications, icon:read" data-hotkey="g n">
          <span class="mail-status all-read"></span>
          <span class="octicon octicon-bell"></span>
</a>  </span>

  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link tooltipped tooltipped-s js-menu-target" href="/new"
       aria-label="Create new…"
       data-ga-click="Header, create new, icon:add">
      <span class="octicon octicon-plus left"></span>
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <ul class="dropdown-menu dropdown-menu-sw">
        
<a class="dropdown-item" href="/new" data-ga-click="Header, create new repository">
  New repository
</a>


  <a class="dropdown-item" href="/organizations/new" data-ga-click="Header, create new organization">
    New organization
  </a>



  <div class="dropdown-divider"></div>
  <div class="dropdown-header">
    <span title="juliomalegria/django-chunked-upload">This repository</span>
  </div>
    <a class="dropdown-item" href="/juliomalegria/django-chunked-upload/issues/new" data-ga-click="Header, create new issue">
      New issue
    </a>

      </ul>
    </div>
  </li>

  <li class="header-nav-item dropdown js-menu-container">
    <a class="header-nav-link name tooltipped tooltipped-sw js-menu-target" href="/Hannu1"
       aria-label="View profile and more"
       data-ga-click="Header, show menu, icon:avatar">
      <img alt="@Hannu1" class="avatar" height="20" src="https://avatars1.githubusercontent.com/u/7165479?v=3&amp;s=40" width="20" />
      <span class="dropdown-caret"></span>
    </a>

    <div class="dropdown-menu-content js-menu-content">
      <div class="dropdown-menu  dropdown-menu-sw">
        <div class=" dropdown-header header-nav-current-user css-truncate">
            Signed in as <strong class="css-truncate-target">Hannu1</strong>

        </div>


        <div class="dropdown-divider"></div>

          <a class="dropdown-item" href="/Hannu1" data-ga-click="Header, go to profile, text:your profile">
            Your profile
          </a>
        <a class="dropdown-item" href="/stars" data-ga-click="Header, go to starred repos, text:your stars">
          Your stars
        </a>
        <a class="dropdown-item" href="/explore" data-ga-click="Header, go to explore, text:explore">
          Explore
        </a>
          <a class="dropdown-item" href="/integrations" data-ga-click="Header, go to integrations, text:integrations">
            Integrations
          </a>
        <a class="dropdown-item" href="https://help.github.com" data-ga-click="Header, go to help, text:help">
          Help
        </a>

          <div class="dropdown-divider"></div>

          <a class="dropdown-item" href="/settings/profile" data-ga-click="Header, go to settings, icon:settings">
            Settings
          </a>

          <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/logout" class="logout-form" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="7erstDEXTGoI8dPVli2VxCE/WuiP7rLX2BCZlJiasikk3Rt7ysDLceX1ecIwnSAzVVOZp9EowT172xS3MG93Qg==" /></div>
            <button class="dropdown-item dropdown-signout" data-ga-click="Header, sign out, icon:logout">
              Sign out
            </button>
</form>
      </div>
    </div>
  </li>
</ul>


    
  </div>
</div>

      

      


    <div id="start-of-content" class="accessibility-aid"></div>

      <div id="js-flash-container">
</div>


    <div role="main" class="main-content">
        <div itemscope itemtype="http://schema.org/WebPage">
    <div id="js-repo-pjax-container" class="context-loader-container js-repo-nav-next" data-pjax-container>
      
<div class="pagehead repohead instapaper_ignore readability-menu experiment-repo-nav">
  <div class="container repohead-details-container">

    

<ul class="pagehead-actions">

  <li>
        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/notifications/subscribe" class="js-social-container" data-autosubmit="true" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="nSY034iJ5dJ+KUORgHQ1YVVFEO6wEmsDXze4r/ma1rS3+t+AitDWcDqUwgNLJRMf9f2Dw4R0EjodL1GY305cxg==" /></div>      <input id="repository_id" name="repository_id" type="hidden" value="11395627" />

        <div class="select-menu js-menu-container js-select-menu">
          <a href="/juliomalegria/django-chunked-upload/subscription"
            class="btn btn-sm btn-with-count select-menu-button js-menu-target" role="button" tabindex="0" aria-haspopup="true"
            data-ga-click="Repository, click Watch settings, action:blob#show">
            <span class="js-select-button">
              <span class="octicon octicon-eye"></span>
              Watch
            </span>
          </a>
          <a class="social-count js-social-count" href="/juliomalegria/django-chunked-upload/watchers">
            2
          </a>

        <div class="select-menu-modal-holder">
          <div class="select-menu-modal subscription-menu-modal js-menu-content" aria-hidden="true">
            <div class="select-menu-header">
              <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
              <span class="select-menu-title">Notifications</span>
            </div>

              <div class="select-menu-list js-navigation-container" role="menu">

                <div class="select-menu-item js-navigation-item selected" role="menuitem" tabindex="0">
                  <span class="select-menu-item-icon octicon octicon-check"></span>
                  <div class="select-menu-item-text">
                    <input checked="checked" id="do_included" name="do" type="radio" value="included" />
                    <span class="select-menu-item-heading">Not watching</span>
                    <span class="description">Be notified when participating or @mentioned.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <span class="octicon octicon-eye"></span>
                      Watch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <span class="select-menu-item-icon octicon octicon octicon-check"></span>
                  <div class="select-menu-item-text">
                    <input id="do_subscribed" name="do" type="radio" value="subscribed" />
                    <span class="select-menu-item-heading">Watching</span>
                    <span class="description">Be notified of all conversations.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <span class="octicon octicon-eye"></span>
                      Unwatch
                    </span>
                  </div>
                </div>

                <div class="select-menu-item js-navigation-item " role="menuitem" tabindex="0">
                  <span class="select-menu-item-icon octicon octicon-check"></span>
                  <div class="select-menu-item-text">
                    <input id="do_ignore" name="do" type="radio" value="ignore" />
                    <span class="select-menu-item-heading">Ignoring</span>
                    <span class="description">Never be notified.</span>
                    <span class="js-select-button-text hidden-select-button-text">
                      <span class="octicon octicon-mute"></span>
                      Stop ignoring
                    </span>
                  </div>
                </div>

              </div>

            </div>
          </div>
        </div>
</form>
  </li>

  <li>
    
  <div class="js-toggler-container js-social-container starring-container ">

    <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/juliomalegria/django-chunked-upload/unstar" class="js-toggler-form starred js-unstar-button" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="pq4rNpXo205/sC4uCSit/AOHbVEzu1r4m85Lwt9WiI1Z3nbTM7LJVz6mKd3z3C3NOKH9OIFidshkWij5mz9IDQ==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Unstar this repository" title="Unstar juliomalegria/django-chunked-upload"
        data-ga-click="Repository, click unstar button, action:blob#show; text:Unstar">
        <span class="octicon octicon-star"></span>
        Unstar
      </button>
        <a class="social-count js-social-count" href="/juliomalegria/django-chunked-upload/stargazers">
          35
        </a>
</form>
    <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/juliomalegria/django-chunked-upload/star" class="js-toggler-form unstarred js-star-button" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" data-remote="true" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="lYvACJMEdCzChdzQVlSEupokEkT5hNyOC6kXS5lp8mwlVOtfDPvLdgY9CsjKVjz8U7l/yntPdgsHF+yLV8KiLg==" /></div>
      <button
        class="btn btn-sm btn-with-count js-toggler-target"
        aria-label="Star this repository" title="Star juliomalegria/django-chunked-upload"
        data-ga-click="Repository, click star button, action:blob#show; text:Star">
        <span class="octicon octicon-star"></span>
        Star
      </button>
        <a class="social-count js-social-count" href="/juliomalegria/django-chunked-upload/stargazers">
          35
        </a>
</form>  </div>

  </li>

  <li>
          <a href="#fork-destination-box" class="btn btn-sm btn-with-count"
              title="Fork your own copy of juliomalegria/django-chunked-upload to your account"
              aria-label="Fork your own copy of juliomalegria/django-chunked-upload to your account"
              rel="facebox"
              data-ga-click="Repository, show fork modal, action:blob#show; text:Fork">
            <span class="octicon octicon-repo-forked"></span>
            Fork
          </a>

          <div id="fork-destination-box" style="display: none;">
            <h2 class="facebox-header" data-facebox-id="facebox-header">Where should we fork this repository?</h2>
            <include-fragment src=""
                class="js-fork-select-fragment fork-select-fragment"
                data-url="/juliomalegria/django-chunked-upload/fork?fragment=1">
              <img alt="Loading" height="64" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-128.gif" width="64" />
            </include-fragment>
          </div>

    <a href="/juliomalegria/django-chunked-upload/network" class="social-count">
      13
    </a>
  </li>
</ul>

    <h1 itemscope itemtype="http://data-vocabulary.org/Breadcrumb" class="entry-title public ">
  <span class="octicon octicon-repo"></span>
  <span class="author"><a href="/juliomalegria" class="url fn" itemprop="url" rel="author"><span itemprop="title">juliomalegria</span></a></span><!--
--><span class="path-divider">/</span><!--
--><strong><a href="/juliomalegria/django-chunked-upload" data-pjax="#js-repo-pjax-container">django-chunked-upload</a></strong>

  <span class="page-context-loader">
    <img alt="" height="16" src="https://assets-cdn.github.com/images/spinners/octocat-spinner-32.gif" width="16" />
  </span>

</h1>

  </div>
  <div class="container">
    
<nav class="reponav js-repo-nav js-sidenav-container-pjax js-octicon-loaders"
     role="navigation"
     data-pjax="#js-repo-pjax-container">

  <a href="/juliomalegria/django-chunked-upload" aria-label="Code" aria-selected="true" class="js-selected-navigation-item selected reponav-item" data-hotkey="g c" data-selected-links="repo_source repo_downloads repo_commits repo_releases repo_tags repo_branches /juliomalegria/django-chunked-upload">
    <span class="octicon octicon-code"></span>
    Code
</a>
    <a href="/juliomalegria/django-chunked-upload/issues" class="js-selected-navigation-item reponav-item" data-hotkey="g i" data-selected-links="repo_issues repo_labels repo_milestones /juliomalegria/django-chunked-upload/issues">
      <span class="octicon octicon-issue-opened"></span>
      Issues
      <span class="counter">2</span>
</a>
  <a href="/juliomalegria/django-chunked-upload/pulls" class="js-selected-navigation-item reponav-item" data-hotkey="g p" data-selected-links="repo_pulls /juliomalegria/django-chunked-upload/pulls">
    <span class="octicon octicon-git-pull-request"></span>
    Pull requests
    <span class="counter">1</span>
</a>
    <a href="/juliomalegria/django-chunked-upload/wiki" class="js-selected-navigation-item reponav-item" data-hotkey="g w" data-selected-links="repo_wiki /juliomalegria/django-chunked-upload/wiki">
      <span class="octicon octicon-book"></span>
      Wiki
</a>
  <a href="/juliomalegria/django-chunked-upload/pulse" class="js-selected-navigation-item reponav-item" data-selected-links="pulse /juliomalegria/django-chunked-upload/pulse">
    <span class="octicon octicon-pulse"></span>
    Pulse
</a>
  <a href="/juliomalegria/django-chunked-upload/graphs" class="js-selected-navigation-item reponav-item" data-selected-links="repo_graphs repo_contributors /juliomalegria/django-chunked-upload/graphs">
    <span class="octicon octicon-graph"></span>
    Graphs
</a>

</nav>

  </div>
</div>

<div class="container new-discussion-timeline experiment-repo-nav">
  <div class="repository-content">

    

<a href="/juliomalegria/django-chunked-upload/blob/56fb303b903fa6f244a301b394e7bd4f05cad06c/README.rst" class="hidden js-permalink-shortcut" data-hotkey="y">Permalink</a>

<!-- blob contrib key: blob_contributors:v21:29e1f8511c193c545816c11884fe4f91 -->

<div class="file-navigation js-zeroclipboard-container">
  
<div class="select-menu js-menu-container js-select-menu left">
  <button class="btn btn-sm select-menu-button js-menu-target css-truncate" data-hotkey="w"
    title="master"
    type="button" aria-label="Switch branches or tags" tabindex="0" aria-haspopup="true">
    <i>Branch:</i>
    <span class="js-select-button css-truncate-target">master</span>
  </button>

  <div class="select-menu-modal-holder js-menu-content js-navigation-container" data-pjax aria-hidden="true">

    <div class="select-menu-modal">
      <div class="select-menu-header">
        <span class="octicon octicon-x js-menu-close" role="button" aria-label="Close"></span>
        <span class="select-menu-title">Switch branches/tags</span>
      </div>

      <div class="select-menu-filters">
        <div class="select-menu-text-filter">
          <input type="text" aria-label="Filter branches/tags" id="context-commitish-filter-field" class="js-filterable-field js-navigation-enable" placeholder="Filter branches/tags">
        </div>
        <div class="select-menu-tabs">
          <ul>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="branches" data-filter-placeholder="Filter branches/tags" class="js-select-menu-tab" role="tab">Branches</a>
            </li>
            <li class="select-menu-tab">
              <a href="#" data-tab-filter="tags" data-filter-placeholder="Find a tag…" class="js-select-menu-tab" role="tab">Tags</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="branches" role="menu">

        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <a class="select-menu-item js-navigation-item js-navigation-open selected"
               href="/juliomalegria/django-chunked-upload/blob/master/README.rst"
               data-name="master"
               data-skip-pjax="true"
               rel="nofollow">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <span class="select-menu-item-text css-truncate-target" title="master">
                master
              </span>
            </a>
        </div>

          <div class="select-menu-no-results">Nothing to show</div>
      </div>

      <div class="select-menu-list select-menu-tab-bucket js-select-menu-tab-bucket" data-tab-filter="tags">
        <div data-filterable-for="context-commitish-filter-field" data-filterable-type="substring">


            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.1.1/README.rst"
                 data-name="1.1.1"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.1.1">1.1.1</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.1.0/README.rst"
                 data-name="1.1.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.1.0">1.1.0</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.0.5/README.rst"
                 data-name="1.0.5"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.5">1.0.5</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.0.4/README.rst"
                 data-name="1.0.4"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.4">1.0.4</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.0.3/README.rst"
                 data-name="1.0.3"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.3">1.0.3</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.0.2/README.rst"
                 data-name="1.0.2"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.2">1.0.2</a>
            </div>
            <div class="select-menu-item js-navigation-item ">
              <span class="select-menu-item-icon octicon octicon-check"></span>
              <a href="/juliomalegria/django-chunked-upload/tree/1.0.0/README.rst"
                 data-name="1.0.0"
                 data-skip-pjax="true"
                 rel="nofollow"
                 class="js-navigation-open select-menu-item-text css-truncate-target"
                 title="1.0.0">1.0.0</a>
            </div>
        </div>

        <div class="select-menu-no-results">Nothing to show</div>
      </div>

    </div>
  </div>
</div>

  <div class="btn-group right">
    <a href="/juliomalegria/django-chunked-upload/find/master"
          class="js-show-file-finder btn btn-sm"
          data-pjax
          data-hotkey="t">
      Find file
    </a>
    <button aria-label="Copy file path to clipboard" class="js-zeroclipboard btn btn-sm zeroclipboard-button tooltipped tooltipped-s" data-copied-hint="Copied!" type="button">Copy path</button>
  </div>
  <div class="breadcrumb js-zeroclipboard-target">
    <span class="repo-root js-repo-root"><span itemscope="" itemtype="http://data-vocabulary.org/Breadcrumb"><a href="/juliomalegria/django-chunked-upload" class="" data-branch="master" data-pjax="true" itemscope="url"><span itemprop="title">django-chunked-upload</span></a></span></span><span class="separator">/</span><strong class="final-path">README.rst</strong>
  </div>
</div>


  <div class="commit-tease">
      <span class="right">
        <a class="commit-tease-sha" href="/juliomalegria/django-chunked-upload/commit/5f4109b924f5086f81fd10da8e85888673780218" data-pjax>
          5f4109b
        </a>
        <time datetime="2015-09-15T19:31:31Z" is="relative-time">Sep 15, 2015</time>
      </span>
      <div>
        <img alt="@juliomalegria" class="avatar" height="20" src="https://avatars3.githubusercontent.com/u/1008637?v=3&amp;s=40" width="20" />
        <a href="/juliomalegria" class="user-mention" rel="author">juliomalegria</a>
          <a href="/juliomalegria/django-chunked-upload/commit/5f4109b924f5086f81fd10da8e85888673780218" class="message" data-pjax="true" title="Make the module independent of a User model
* Some projects don&#39;t have a User model, and django-chunked-upload should work for them too.
* Created a base model (`BaseChunkedUpload`), which doesn&#39;t have a FK to the User model. This model will always be abstract. The old `ChunkedUpload` remains unchanged, with a FK to the User model. If it fits your needs, use it making it not abstract on your settings.
* If an md5 doesn&#39;t match, the request will still fail, but won&#39;t mark the chunked upload as FAILED (I removed the FAILED status completely).

Bumped up version to `1.1.0`.">Make the module independent of a User model</a>
      </div>

    <div class="commit-tease-contributors">
      <a class="muted-link contributors-toggle" href="#blob_contributors_box" rel="facebox">
        <strong>1</strong>
         contributor
      </a>
      
    </div>

    <div id="blob_contributors_box" style="display:none">
      <h2 class="facebox-header" data-facebox-id="facebox-header">Users who have contributed to this file</h2>
      <ul class="facebox-user-list" data-facebox-id="facebox-description">
          <li class="facebox-user-list-item">
            <img alt="@juliomalegria" height="24" src="https://avatars1.githubusercontent.com/u/1008637?v=3&amp;s=48" width="24" />
            <a href="/juliomalegria">juliomalegria</a>
          </li>
      </ul>
    </div>
  </div>

<div class="file">
  <div class="file-header">
  <div class="file-actions">

    <div class="btn-group">
      <a href="/juliomalegria/django-chunked-upload/raw/master/README.rst" class="btn btn-sm " id="raw-url">Raw</a>
        <a href="/juliomalegria/django-chunked-upload/blame/master/README.rst" class="btn btn-sm js-update-url-with-hash">Blame</a>
      <a href="/juliomalegria/django-chunked-upload/commits/master/README.rst" class="btn btn-sm " rel="nofollow">History</a>
    </div>

        <a class="octicon-btn tooltipped tooltipped-nw"
           href="github-windows://openRepo/https://github.com/juliomalegria/django-chunked-upload?branch=master&amp;filepath=README.rst"
           aria-label="Open this file in GitHub Desktop"
           data-ga-click="Repository, open with desktop, type:windows">
            <span class="octicon octicon-device-desktop"></span>
        </a>

        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/juliomalegria/django-chunked-upload/edit/master/README.rst" class="inline-form js-update-url-with-hash" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="JAXBIdxl+IQhD+gzyuEKVT9pjKY3N/f8ZBsxFZQzugCRZvG+ctvqw8Z5Kla8T0Cj7Q+4Ld/4Oo6eOSMI0GW71w==" /></div>
          <button class="octicon-btn tooltipped tooltipped-nw" type="submit"
            aria-label="Fork this project and edit the file" data-hotkey="e" data-disable-with>
            <span class="octicon octicon-pencil"></span>
          </button>
</form>        <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="/juliomalegria/django-chunked-upload/delete/master/README.rst" class="inline-form" data-form-nonce="c44ff91b7710a1e032987c1f3b1a1060710971b9" method="post"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /><input name="authenticity_token" type="hidden" value="596aaanYXwhkpUo3/qxt2IpmXHLFtq2lCKgnkksjlijaO1bpxBhWSu59F9gLlswMDO7/lupkXmmFrOIXgU7D2w==" /></div>
          <button class="octicon-btn octicon-btn-danger tooltipped tooltipped-nw" type="submit"
            aria-label="Fork this project and delete the file" data-disable-with>
            <span class="octicon octicon-trashcan"></span>
          </button>
</form>  </div>

  <div class="file-info">
      142 lines (92 sloc)
      <span class="file-info-divider"></span>
    4.49 KB
  </div>
</div>

  
  <div id="readme" class="blob instapaper_body">
    <article class="markdown-body entry-content" itemprop="mainContentOfPage"><h1><a id="user-content-django-chunked-upload" class="anchor" href="#django-chunked-upload" aria-hidden="true"><span class="octicon octicon-link"></span></a>django-chunked-upload</h1>
<p>This simple django app enables users to upload large files to Django in multiple chunks, with the ability to resume if the upload is interrupted.</p>
<p>This app is intented to work with <a href="https://github.com/blueimp/jQuery-File-Upload">JQuery-File-Upload</a> by <a href="https://blueimp.net">Sebastian Tschan</a> (<a href="https://github.com/blueimp/jQuery-File-Upload/wiki">documentation</a>).</p>
<p>License: <a href="https://romanrm.net/mit-zero">MIT-Zero</a>.</p>
<a name="user-content-demo"></a>
<h2><a id="user-content-demo" class="anchor" href="#demo" aria-hidden="true"><span class="octicon octicon-link"></span></a>Demo</h2>
<p>If you want to see a very simple Django demo project using this module, please take a look at <a href="https://github.com/juliomalegria/django-chunked-upload-demo">django-chunked-upload-demo</a>.</p>
<a name="user-content-installation"></a>
<h2><a id="user-content-installation" class="anchor" href="#installation" aria-hidden="true"><span class="octicon octicon-link"></span></a>Installation</h2>
<p>Install via pip:</p>
<pre>pip install django-chunked-upload
</pre>
<p>And then add it to your Django <code>INSTALLED_APPS</code>:</p>
<div class="highlight highlight-source-python"><pre>INSTALLED_APPS <span class="pl-k">=</span> (
    <span class="pl-c"># ...</span>
    <span class="pl-s"><span class="pl-pds">'</span>chunked_upload<span class="pl-pds">'</span></span>,
)</pre></div>
<a name="user-content-typical-usage"></a>
<h2><a id="user-content-typical-usage" class="anchor" href="#typical-usage" aria-hidden="true"><span class="octicon octicon-link"></span></a>Typical usage</h2>
<ol>
<li>An initial POST request is sent to the url linked to <code>ChunkedUploadView</code> (or any subclass) with the first chunk of the file. The name of the chunk file can be overriden in the view (class attribute <code>field_name</code>). Example:</li>
</ol>
<pre>{"my_file": &lt;File&gt;}
</pre>
<ol start="2">
<li>In return, server with response with the <code>upload_id</code>, the current <code>offset</code> and the when will the upload expire (<code>expires</code>). Example:</li>
</ol>
<pre>{
    "upload_id": "5230ec1f59d1485d9d7974b853802e31",
    "offset": 10000,
    "expires": "2013-07-18T17:56:22.186Z"
}
</pre>
<ol start="3">
<li>Repeatedly POST subsequent chunks using the <code>upload_id</code> to identify the upload  to the url linked to <code>ChunkedUploadView</code> (or any subclass). Example:</li>
</ol>
<pre>{
    "upload_id": "5230ec1f59d1485d9d7974b853802e31",
    "my_file": &lt;File&gt;
}
</pre>
<ol start="4">
<li>Server will continue responding with the <code>upload_id</code>, the current <code>offset</code> and the expiration date (<code>expires</code>).</li>
<li>Finally, when upload is completed, a POST request is sent to the url linked to <code>ChunkedUploadCompleteView</code> (or any subclass). This request must include the <code>upload_id</code> and the <code>md5</code> checksum (hex). Example:</li>
</ol>
<pre>{
    "upload_id": "5230ec1f59d1485d9d7974b853802e31",
    "md5": "fc3ff98e8c6a0d3087d515c0473f8677"
}
</pre>
<ol start="6">
<li>If everything is OK, server will response with status code 200 and the data returned in the method <code>get_response_data</code> (if any).</li>
</ol>
<a name="user-content-possible-error-responses"></a>
<h3><a id="user-content-possible-error-responses" class="anchor" href="#possible-error-responses" aria-hidden="true"><span class="octicon octicon-link"></span></a>Possible error responses:</h3>
<ul>
<li>User is not authenticated. Server responds 403 (Forbidden).</li>
<li>Upload has expired. Server responds 410 (Gone).</li>
<li><code>upload_id</code> does not match any upload. Server responds 404 (Not found).</li>
<li>No chunk file is found in the indicated key. Server responds 400 (Bad request).</li>
<li>Request does not contain <code>Content-Range</code> header. Server responds 400 (Bad request).</li>
<li>Size of file exceeds limit (if specified).  Server responds 400 (Bad request).</li>
<li>Offsets does not match.  Server responds 400 (Bad request).</li>
<li><code>md5</code> checksums does not match. Server responds 400 (Bad request).</li>
</ul>
<a name="user-content-settings"></a>
<h2><a id="user-content-settings" class="anchor" href="#settings" aria-hidden="true"><span class="octicon octicon-link"></span></a>Settings</h2>
<p>Add any of these variables into your project settings to override them.</p>
<a name="user-content-chunked-upload-expiration-delta"></a>
<h3><a id="user-content-chunked_upload_expiration_delta" class="anchor" href="#chunked_upload_expiration_delta" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_EXPIRATION_DELTA</code></h3>
<ul>
<li>How long after creation the upload will expire.</li>
<li>Default: <code>datetime.timedelta(days=1)</code></li>
</ul>
<a name="user-content-chunked-upload-path"></a>
<h3><a id="user-content-chunked_upload_path" class="anchor" href="#chunked_upload_path" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_PATH</code></h3>
<ul>
<li>Path where uploading files will be stored until completion.</li>
<li>Default: <code>'chunked_uploads/%Y/%m/%d'</code></li>
</ul>
<a name="user-content-chunked-upload-storage-class"></a>
<h3><a id="user-content-chunked_upload_storage_class" class="anchor" href="#chunked_upload_storage_class" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_STORAGE_CLASS</code></h3>
<ul>
<li>Storage system (should be a class).</li>
<li>Default: <code>None</code> (use default storage system)</li>
</ul>
<a name="user-content-chunked-upload-abstract-model"></a>
<h3><a id="user-content-chunked_upload_abstract_model" class="anchor" href="#chunked_upload_abstract_model" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_ABSTRACT_MODEL</code></h3>
<ul>
<li>Boolean that defines if the <code>ChunkedUpload</code> model will be abstract or not (<a href="https://docs.djangoproject.com/en/1.4/ref/models/options/#abstract">what does abstract model mean?</a>).</li>
<li>Default: <code>True</code></li>
</ul>
<a name="user-content-chunked-upload-encoder"></a>
<h3><a id="user-content-chunked_upload_encoder" class="anchor" href="#chunked_upload_encoder" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_ENCODER</code></h3>
<ul>
<li>Function used to encode response data. Receives a dict and returns a string.</li>
<li>Default: <code>DjangoJSONEncoder().encode</code></li>
</ul>
<a name="user-content-chunked-upload-content-type"></a>
<h3><a id="user-content-chunked_upload_content_type" class="anchor" href="#chunked_upload_content_type" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_CONTENT_TYPE</code></h3>
<ul>
<li>Content-Type for the response data.</li>
<li>Default: <code>'application/json'</code></li>
</ul>
<a name="user-content-chunked-upload-mimetype"></a>
<h3><a id="user-content-chunked_upload_mimetype" class="anchor" href="#chunked_upload_mimetype" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_MIMETYPE</code></h3>
<ul>
<li><strong>Deprecated</strong>, use <code>CHUNKED_UPLOAD_CONTENT_TYPE</code> instead.</li>
</ul>
<a name="user-content-chunked-upload-max-bytes"></a>
<h3><a id="user-content-chunked_upload_max_bytes" class="anchor" href="#chunked_upload_max_bytes" aria-hidden="true"><span class="octicon octicon-link"></span></a><code>CHUNKED_UPLOAD_MAX_BYTES</code></h3>
<ul>
<li>Max amount of data (in bytes) that can be uploaded. <code>None</code> means no limit.</li>
<li>Default: <code>None</code></li>
</ul>
<a name="user-content-support"></a>
<h2><a id="user-content-support" class="anchor" href="#support" aria-hidden="true"><span class="octicon octicon-link"></span></a>Support</h2>
<p>If you find any bug or you want to propose a new feature, please use the <a href="https://github.com/juliomalegria/django-chunked-upload/issues">issues tracker</a>. I'll be happy to help you! :-)</p>

</article>
  </div>

</div>

<a href="#jump-to-line" rel="facebox[.linejump]" data-hotkey="l" style="display:none">Jump to Line</a>
<div id="jump-to-line" style="display:none">
  <!-- </textarea> --><!-- '"` --><form accept-charset="UTF-8" action="" class="js-jump-to-line-form" method="get"><div style="margin:0;padding:0;display:inline"><input name="utf8" type="hidden" value="&#x2713;" /></div>
    <input class="linejump-input js-jump-to-line-field" type="text" placeholder="Jump to line&hellip;" aria-label="Jump to line" autofocus>
    <button type="submit" class="btn">Go</button>
</form></div>

  </div>
  <div class="modal-backdrop"></div>
</div>

    </div>
  </div>

    </div>

        <div class="container">
  <div class="site-footer" role="contentinfo">
    <ul class="site-footer-links right">
        <li><a href="https://status.github.com/" data-ga-click="Footer, go to status, text:status">Status</a></li>
      <li><a href="https://developer.github.com" data-ga-click="Footer, go to api, text:api">API</a></li>
      <li><a href="https://training.github.com" data-ga-click="Footer, go to training, text:training">Training</a></li>
      <li><a href="https://shop.github.com" data-ga-click="Footer, go to shop, text:shop">Shop</a></li>
        <li><a href="https://github.com/blog" data-ga-click="Footer, go to blog, text:blog">Blog</a></li>
        <li><a href="https://github.com/about" data-ga-click="Footer, go to about, text:about">About</a></li>
        <li><a href="https://github.com/pricing" data-ga-click="Footer, go to pricing, text:pricing">Pricing</a></li>

    </ul>

    <a href="https://github.com" aria-label="Homepage">
      <span class="mega-octicon octicon-mark-github" title="GitHub"></span>
</a>
    <ul class="site-footer-links">
      <li>&copy; 2015 <span title="0.08993s from github-fe119-cp1-prd.iad.github.net">GitHub</span>, Inc.</li>
        <li><a href="https://github.com/site/terms" data-ga-click="Footer, go to terms, text:terms">Terms</a></li>
        <li><a href="https://github.com/site/privacy" data-ga-click="Footer, go to privacy, text:privacy">Privacy</a></li>
        <li><a href="https://github.com/security" data-ga-click="Footer, go to security, text:security">Security</a></li>
        <li><a href="https://github.com/contact" data-ga-click="Footer, go to contact, text:contact">Contact</a></li>
        <li><a href="https://help.github.com" data-ga-click="Footer, go to help, text:help">Help</a></li>
    </ul>
  </div>
</div>



    
    
    

    <div id="ajax-error-message" class="flash flash-error">
      <span class="octicon octicon-alert"></span>
      <button type="button" class="flash-close js-flash-close js-ajax-error-dismiss" aria-label="Dismiss error">
        <span class="octicon octicon-x"></span>
      </button>
      Something went wrong with that request. Please try again.
    </div>


      <script crossorigin="anonymous" integrity="sha256-t8lSPZPmzQI1oKi30aaR95CdODTNnJyqexZ0ulCLZEw=" src="https://assets-cdn.github.com/assets/frameworks-b7c9523d93e6cd0235a0a8b7d1a691f7909d3834cd9c9caa7b1674ba508b644c.js"></script>
      <script async="async" crossorigin="anonymous" integrity="sha256-R6f9HHK06U+YqQiEkQu1Sw+/g2FKCcPgmAGZvFyAErY=" src="https://assets-cdn.github.com/assets/github-47a7fd1c72b4e94f98a90884910bb54b0fbf83614a09c3e0980199bc5c8012b6.js"></script>
      
      
      
    <div class="js-stale-session-flash stale-session-flash flash flash-warn flash-banner hidden">
      <span class="octicon octicon-alert"></span>
      <span class="signed-in-tab-flash">You signed in with another tab or window. <a href="">Reload</a> to refresh your session.</span>
      <span class="signed-out-tab-flash">You signed out in another tab or window. <a href="">Reload</a> to refresh your session.</span>
    </div>
  </body>
</html>

