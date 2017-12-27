/*
    This code is from Dynamic Web Coding at dyn-web.com
    Copyright 2009-12 by Sharon Paine 
    See Terms of Use at www.dyn-web.com/business/terms.php
    regarding conditions under which you may use this code.
    This notice must be retained in the code as is!
*/

// DYN_WEB is namespace used for code from dyn-web.com
// replacing previous use of dw_ prefix for object names
var DYN_WEB = DYN_WEB || {};

DYN_WEB.Event={add:document.addEventListener?function(obj,etype,fp,cap){cap=cap||false;obj.addEventListener(etype,fp,cap);}:function(obj,etype,fp){obj.attachEvent("on"+etype,fp);},remove:document.removeEventListener?function(obj,etype,fp,cap){cap=cap||false;obj.removeEventListener(etype,fp,cap);}:function(obj,etype,fp){obj.detachEvent("on"+etype,fp);},DOMit:function(e){e=e?e:window.event;if(!e.target)e.target=e.srcElement;if(!e.preventDefault)e.preventDefault=function(){e.returnValue=false;return false;};if(!e.stopPropagation)e.stopPropagation=function(){e.cancelBubble=true;};return e;},getTarget:function(e){e=dw_Event.DOMit(e);var tgt=e.target;if(tgt.nodeType!=1)tgt=tgt.parentNode;return tgt;}};

DYN_WEB.Cookie={set:function(name,value,days,path,domain,secure){var date,expires;if(typeof days=="number"){date=new Date();date.setTime(date.getTime()+(days*24*60*60*1000));expires=date.toGMTString();}document.cookie=name+"="+encodeURIComponent(value)+((expires)?"; expires="+expires:"")+((path)?"; path="+path:"")+((domain)?"; domain="+domain:"")+((secure)?"; secure":"");},get:function(name){var c,cookies=document.cookie.split(/;\s/g);for(var i=0;cookies[i];i++){c=cookies[i];if(c.indexOf(name+'=')===0){return decodeURIComponent(c.slice(name.length+1,c.length));}}return null;},del:function(name,path,domain){if(dw_Cookie.get(name)){document.cookie=name+"="+((path)?"; path="+path:"")+((domain)?"; domain="+domain:"")+"; expires=Thu, 01-Jan-70 00:00:01 GMT";}}};

if ( !DYN_WEB.Util ) {
    DYN_WEB.Util = {
        // add props of Obj2 to Obj1
        augment: function(Obj1, Obj2) {
            var prop;
            for ( prop in Obj2 ) {
                if ( Obj2.hasOwnProperty(prop) && !Obj1[prop] ) {
                    Obj1[prop] = Obj2[prop];                
                }
            }
        },
        $: function(id){
            return document.getElementById(id);
        }
    };
}

DYN_WEB.Tabs = (function(){
    
    // obj holds props: id, useCookies, etc.
    function Constr(obj) {
        this.useCookies = obj.useCookies;
        this.before_hide = obj.before_hide || function(){};
        this.on_activate = obj.on_activate || function(){};
        this.on_init = obj.on_init || function(){};
        Constr.col[obj.id] = this;
        Constr.init(obj.id);
    }
    
    Constr.col = {};
    
    Constr.prototype = {
        current: null // id of currently active pane
    }
    
    return Constr;
})();

(function(){
    var Ut = DYN_WEB.Util,
        Ev = DYN_WEB.Event,
        Cookie = DYN_WEB.Cookie,
        Tabs = DYN_WEB.Tabs; 
    
    Ut.augment(Tabs, {
        // static props/methods for DYN_WEB.Tabs
        setup: function(){
            var obj, settings = [];
            if ( Tabs.hasBrowserSupport() ) {
                for (var i=0; obj = arguments[i]; i++) {
                    if ( obj.css ) {
                        Ut.writeStyleSheet(obj.css);
                    }
                    settings[i] = obj; // save to pass to constructor onload
                }
                Ev.add(window, 'load', function(){
                    for (var i=0; settings[i]; i++) {
                        new Tabs( settings[i] );
                    }
                });
            }
        },
        hasBrowserSupport: function(){
            if ( document.getElementById && document.getElementsByTagName 
                 && typeof decodeURI !== 'undefined'
                 && (document.addEventListener || document.attachEvent) ) {
                return true;
            }
            return false;
        },
        
        init: function(tabsetId){
            var _this = Tabs.col[tabsetId],
                links = Tabs.getTabs(tabsetId),
                // code uses hash in tab links but tabs can also link to other pages
                // so compare current location to link's href
                loc = Ut.getURLtoHash(location),
                lnk, pg, paneId, pane, sel, dflt, cur, c, q, hash;
                
            q = Ut.getValueFromQueryString(tabsetId); 
            if (_this.useCookies) {
                c = Tabs.checkCookie(tabsetId);
            }
            // tab in query string or cookie?
            sel = q? q: c? c: null;
                
            // add ids and event handlers to links ...
            for (var i=0; lnk = links[i]; i++) {
                paneId = '', pane = ''; // reset
                pg = Ut.getURLtoHash(lnk);
                hash = Ut.getHash(lnk);
                if ( lnk.hash && (loc == pg) ) { // has hash and points to current page
                    paneId = hash;
                    lnk.id = tabsetId + '__' + paneId; // double underscore between
                }
                // if tab associated with tabpane, set up onclick fn
                if (paneId) { 
                    try {
                        pane = Ut.$(paneId);    
                    } catch (err) { // showClicked fn throws
                    }
                    
                    // first tab/pane is default 
                    if ( !dflt ) {
                        dflt = paneId;
                    }
                    
                    // if set active in markup, hold as current
                    if ( pane && Ut.hasClass(lnk, 'activeTab') && Ut.hasClass( pane, 'activePane') ) {
                        _this.current = cur = paneId;
                    }
                
                    // to pass paneId, tabsetId to showClicked...
                    Ev.add( lnk, 'click', function(paneId, tabsetId){
                            return  function(e){
                                Tabs.showClicked(e, paneId, tabsetId);
                            }
                        }(paneId, tabsetId) );
                }
            }

            // check if tab and pane for sel
            if ( sel && (lnk = Ut.$(tabsetId + '__' + sel) ) && (pane = Ut.$(sel) ) ) {
                if ( cur && cur !== sel ) {
                    Tabs.hideCurrent(tabsetId, cur);
                }
                Ut.addClass(lnk, 'activeTab');
                Ut.addClass(pane, 'activePane');
                _this.current = sel;
            } else if ( !cur && dflt ) {
                Ut.addClass( Ut.$( tabsetId + '__' + dflt), 'activeTab' );
                Ut.addClass( Ut.$(dflt), 'activePane' );
                _this.current = dflt;
            }
            _this.on_init();
        },
        
        getTabs: function(id){
            var set = Ut.$(id), list, links;
            if ( !set ) {
                throw new Error('No element matching tabset id found.');
                return [];
            }
            list = Ut.getElementsByClassName('tabnavs', 'ul',  set);
            if ( list.length === 0 ) {
                throw new Error('No tabnavs were found in the tabset.');
                return [];
            }
            links = list[0].getElementsByTagName('a'); 
            return links;
        },
        
        showClicked: function(e, paneId, tabsetId){
            var tabId = tabsetId + '__' + paneId;
            var _this = Tabs.col[tabsetId];
            _this.before_hide(tabId, paneId, tabsetId);
            Tabs.hideCurrent(tabsetId, _this.current);
            Ut.addClass( Ut.$(tabId), 'activeTab');
            
            try {
                Ut.addClass(Ut.$(paneId), 'activePane');
            } catch (err) {
                throw new Error('showClicked can\'t find pane associated with tab. Check tab hash and pane id.');
                return false;
            }
            
            _this.current = paneId;
            if ( _this.useCookies ) {
                Tabs.setCookie(tabsetId, paneId);
            }
            
            _this.on_activate(tabId, paneId, tabsetId);
            if (e) {
                Ev.DOMit(e);
                e.preventDefault();
            }
            return false;
        },
        
        hideCurrent: function(tabsetId, cur) {
            var tab = Ut.$( tabsetId + '__' + cur ),
                pane = Ut.$( cur );
            Ut.removeClass( tab, 'activeTab' );
            Ut.removeClass( pane, 'activePane' );
        },
        
        checkCookie: function(tabsetId) {
            var c, cookies, tab_cookies = Cookie.get('dw_Tabs');
            if ( tab_cookies ) {
                cookies = tab_cookies.split(',');
                for (var i=0; cookies[i]; i++) {
                    c = cookies[i];
                    if ( c.indexOf(tabsetId + ':') === 0 ) {
                        return decodeURI( c.slice(tabsetId.length + 1, c.length) );
                    }
                }
            }
            return null;
        },
        
        setCookie: function(tabsetId, paneId) {
            // format for cookies (multiple tabsets supported): dw_Tabs=tabsetId:paneId,tabsetId:paneId;
            var new_tab_cookies = '', cookies,
                tab_cookies = Cookie.get('dw_Tabs');
            if ( tab_cookies ) {
                cookies = tab_cookies.split(',');
                for (var i=0; cookies[i]; i++) {
                    if ( cookies[i].indexOf(tabsetId + ':') === 0 ) {
                        cookies[i] = tabsetId + ':' + paneId;
                        new_tab_cookies = cookies.join(',');
                        break;
                    }
                }
                if ( !new_tab_cookies ) { // if no match for this tabsetId
                    new_tab_cookies = tab_cookies + ',' + tabsetId + ':' + paneId;
                }
            } else { // no dw_Tabs set yet
                new_tab_cookies = tabsetId + ':' + paneId;
            }
            Cookie.set('dw_Tabs', new_tab_cookies, null, '/');
        }
        
    });
})(); 


// util

(function(){
    var Ut = DYN_WEB.Util;
    // add methods to DYN_WEB.Util
    Ut.augment(Ut, {
        trim: function(str) {
            if ( String.prototype.trim ) {
                return str.trim(); // ECMAScript 5
            } else {
                var re = /^\s+|\s+$/g;
                return str.replace(re, "");    
            }
        },
    
        normalizeString: function(str) {
            var re = /\s\s+/g;
            return Ut.trim(str).replace(re, " ");
        },
        
        hasClass: function(el, cl) {
            var re = new RegExp("\\b" + cl + "\\b", "i");
            if ( re.test( el.className ) ) {
                return true;
            }
            return false;
        },
    
        addClass: function(el, cl) {
            if ( !Ut.hasClass(el, cl) ) {
                el.className = Ut.trim( el.className + ' ' + cl );
            }
        },
    
        removeClass: function(el, cl) {
            el.className = Ut.normalizeString( el.className.replace(cl, " ") );
        },
        
        getElementsByClassName: function (sClass, sTag, oCont) {
            oCont = oCont? oCont: document;
            if ( oCont.getElementsByClassName ) {
                return oCont.getElementsByClassName(sClass); // html5
            } else {
                sTag = sTag || '*';
                var result = [],
                    re = new RegExp("\\b" + sClass + "\\b", "i"),
                    list = oCont.getElementsByTagName(sTag);
                for (var i=0; list[i]; i++) {
                    if ( re.test( list[i].className ) ) result.push( list[i] );
                }
                return result;
            }
        },
        
        // obj: link or window.location
        getValueFromQueryString: function (name, obj) {
            obj = obj? obj: window.location; 
            var pairs, set;
            if (obj.search && obj.search.indexOf(name != -1) ) {
                pairs = obj.search.slice(1).split("&"); // name/value pairs
                for (var i=0; pairs[i]; i++) {
                    set = pairs[i].split("="); // Check each pair for match on name 
                    if ( set[0] == name && set[1] ) {
                        return set[1];
                    }
                }
            }
            return '';
        },
        
        getURLtoHash: function(obj) {
            obj = obj? obj: window.location; 
            var href = obj.href, 
                pt = href.indexOf('#'),
                url = (pt != -1)? href.slice(0, pt): href; // remove hash from href 
            return url;
        },
        
        getHash: function(obj){
            obj = obj? obj: window.location; 
            var hash = '';
            if ( obj.hash ) { // some browsers say true if just #, some '' (ff)
                hash = obj.hash.slice(1);
            }
            return hash;
        },
        
        // Alternate functions are available that use DOM methods instead of document.write
        writeStyleSheet: function(file, bScreen) {
            var screen = (bScreen != false)? '" media="screen" />\n': '"/>\n';
            document.write( '\n<link rel="stylesheet" href="' + file + screen);
        },
        
        // used to set min-height (as on dyn-web home page)
        writeStyleRule: function(rule, bScreen) {
            var screen = (bScreen != false)? ' media="screen">': '>';
            document.write( '\n<style type="text/css"' + screen + rule + '</style>');
        }
    });
})();
