/**
 * Galleria Twelve Theme - v1.5 2017-05-10
 * https://galleria.io
 *
 * Copyright (c) 2010 - 2017 worse is better UG
 * LICENSE: 6fa326ed97f0ac086e1d4bac00db0933
 * https://galleria.io/license/
 *
 */

! function(a) {
    Galleria.addTheme({
        name: "twelve",
        version: 1.5,
        author: "Galleria",
        css: "galleria.twelve.min.css?v=1.5",
        defaults: {
            transition: "pulse",
            transitionSpeed: 500,
            imageCrop: !0,
            thumbCrop: !0,
            carousel: !1,
            _locale: {
                show_thumbnails: "Show thumbnails",
                hide_thumbnails: "Hide thumbnails",
                play: "Play slideshow",
                pause: "Pause slideshow",
                enter_fullscreen: "Enter fullscreen",
                exit_fullscreen: "Exit fullscreen",
                popout_image: "Popout image",
                showing_image: "Showing image %s of %s"
            },
            _showFullscreen: !0,
            _showPopout: !0,
            _showProgress: !0,
            _showTooltip: !0
        },
        init: function(b) {
            Galleria.requires(1.5, "This version of Twelve theme requires Galleria version 1.5 or later"), this.addElement("bar", "fullscreen", "play", "popout", "thumblink", "s1", "s2", "s3", "s4", "progress"), this.append({
                stage: "progress",
                container: ["bar", "tooltip"],
                bar: ["fullscreen", "play", "popout", "thumblink", "info", "s1", "s2", "s3", "s4"]
            }), this.prependChild("info", "counter");
            var c = this,
                d = this.$("thumbnails-container"),
                e = this.$("thumblink"),
                f = this.$("fullscreen"),
                g = this.$("play"),
                h = this.$("popout"),
                i = this.$("bar"),
                j = this.$("progress"),
                k = b.transition,
                l = b._locale,
                m = !1,
                n = !1,
                o = !!b.autoplay,
                p = !1,
                q = function() {
                    d.height(c.getStageHeight()).width(c.getStageWidth()).css("top", m ? 0 : c.getStageHeight() + 30)
                },
                r = function(a) {
                    m && p ? c.play() : (p = o, c.pause()), Galleria.utils.animate(d, {
                        top: m ? c.getStageHeight() + 30 : 0
                    }, {
                        easing: "galleria",
                        duration: 400,
                        complete: function() {
                            c.defineTooltip("thumblink", m ? l.show_thumbnails : l.hide_thumbnails), e[m ? "removeClass" : "addClass"]("open"), m = !m
                        }
                    })
                };
            q(), b._showTooltip && c.bindTooltip({
                thumblink: l.show_thumbnails,
                fullscreen: l.enter_fullscreen,
                play: function() {
                    return o ? l.pause : l.play
                },
                popout: l.popout_image,
                caption: function() {
                    var a = c.getData(),
                        b = "";
                    return a && (a.title && a.title.length && (b += "<strong>" + a.title + "</strong>"), a.description && a.description.length && (b += "<br>" + a.description)), b
                },
                counter: function() {
                    return l.showing_image.replace(/\%s/, c.getIndex() + 1).replace(/\%s/, c.getDataLength())
                }
            }), b.showInfo || this.$("info").hide(), this.bind("play", function() {
                o = !0, g.addClass("playing")
            }), this.bind("pause", function() {
                o = !1, g.removeClass("playing"), j.width(0)
            }), b._showProgress && this.bind("progress", function(a) {
                j.width(a.percent / 100 * this.getStageWidth())
            }), this.bind("loadstart", function(a) {
                a.cached || this.$("loader").show()
            }), this.bind("loadfinish", function(a) {
                j.width(0), this.$("loader").hide(), this.refreshTooltip("counter", "caption")
            }), this.bind("thumbnail", function(b) {
                a(b.thumbTarget).hover(function() {
                    c.setInfo(b.thumbOrder), c.setCounter(b.thumbOrder)
                }, function() {
                    c.setInfo(), c.setCounter()
                }).on("click:fast", function() {
                    r()
                })
            }), this.bind("fullscreen_enter", function(a) {
                n = !0, c.setOptions("transition", !1), f.addClass("open"), i.css("bottom", 0), this.defineTooltip("fullscreen", l.exit_fullscreen), Galleria.TOUCH || this.addIdleState(i, {
                    bottom: -31
                })
            }), this.bind("fullscreen_exit", function(a) {
                n = !1, Galleria.utils.clearTimer("bar"), c.setOptions("transition", k), f.removeClass("open"), i.css("bottom", 0), this.defineTooltip("fullscreen", l.enter_fullscreen), Galleria.TOUCH || this.removeIdleState(i, {
                    bottom: -31
                })
            }), this.bind("rescale", q), Galleria.TOUCH || (this.addIdleState(this.get("image-nav-left"), {
                left: -36
            }), this.addIdleState(this.get("image-nav-right"), {
                right: -36
            })), e.on("click:fast", r), b.thumbnails || (e.hide(), g.css("left", 0), this.$("s2").hide(), this.$("info").css("left", 41)), b._showPopout ? h.on("click:fast", function(a) {
                c.openLightbox(), a.preventDefault()
            }) : (h.remove(), b._showFullscreen && (this.$("s4").remove(), this.$("info").css("right", 40), f.css("right", 0))), g.on("click:fast", function() {
                o ? c.pause() : (m && e.trigger("click:fast"), c.play())
            }), b._showFullscreen ? f.on("click:fast", function() {
                if (n) {
                    c.exitFullscreen()
                } else {
                    c.enterFullscreen();
                    c.enterFullscreen();
                }
            }) : (f.remove(), b._show_popout && (this.$("s4").remove(), this.$("info").css("right", 40), h.css("right", 0))), b._showFullscreen || b._showPopout || (this.$("s3,s4").remove(), this.$("info").css("right", 10)), b.autoplay && this.trigger("play")
        }
    })
}(jQuery);
