# /etc/varnish/default.vcl
import std;
include "/docker/varnish/accept-language.vcl";

backend default {
    .host = "nginx";
    .port = "8080";
}

sub vcl_recv {
    # Uncomment the following lines to redirect non-https to https
    #if (req.http.X-Forwarded-Proto !~ "(?i)https") {
    #    set req.http.x-Redir-Url = "https://www.{{project}}.dev" + req.url;
    #    error 750 req.http.x-Redir-Url;
    #}

    # Pass static files to Nginx
    if (req.url ~ "\.(jpg|jpeg|png|gif|css|js)$") {
        /* Remove the cookie and make the request static */
        unset req.http.cookie;
        return (pass);
    }

	# Rewrite Accept-Language
	set req.http.X-Varnish-Accept-Language = req.http.Accept-Language;
	C{
		vcl_rewrite_accept_language(sp);
	}C

	# If language is set in cookie, put it's value into X-Varnish-Accept-Language
	if (req.http.cookie ~ "language=") {
		set req.http.X-Varnish-Accept-Language = regsub(req.http.cookie, "(.*?)(language=)([^;]*)(.*)$", "\3");
    }
    set req.http.Accept-Language = req.http.X-Varnish-Accept-Language;

    # Remove all cookies except csrftoken and sessionid
    if (req.http.Cookie) {
	    set req.http.Cookie = ";" + req.http.Cookie;
	    set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
	    set req.http.Cookie = regsuball(req.http.Cookie, ";(csrftoken|sessionid)=", "; \1=");
	    set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
	    set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

	    if (req.http.Cookie == "") {
	        remove req.http.Cookie;
	    }
	}

	# Remove double // in urls,
	set req.url = regsuball(req.url, "//", "/");

	# Add client IP
	if (req.restarts == 0) {
		if (req.http.X-Forwarded-For) {
			set req.http.X-Forwarded-For = req.http.X-Forwarded-For + ", " + client.ip;
		} else {
			set req.http.X-Forwarded-For = client.ip;
		}
	}

	# Rewrite Accept-Encoding
	if (req.http.Accept-Encoding) {
		if (req.http.Accept-Encoding ~ "gzip") {
			set req.http.Accept-Encoding = "gzip";
		} else {
			remove req.http.Accept-Encoding;
		}
	}

	if (req.http.Authorization || req.url ~ "^/admin") {
		return(pass);
  	}
  	return(lookup);
}

sub vcl_fetch {
    # Uncomment to perform ESI
    #set beresp.do_esi = true;

    if (beresp.http.X-Cache-Vary){
		set beresp.http.Vary = beresp.http.X-Cache-Vary;
	} else if (req.url ~ "^/esi") {
        # ESI urls vary also on Cookie (important!)
        set beresp.http.Vary = "Cookie, Accept-Language, Accept-Encoding";
	} else {
		set beresp.http.Vary = "Accept-Encoding";
	}

	if (beresp.http.X-Cache-TTL){
		set beresp.ttl = std.duration(beresp.http.X-Cache-TTL, 0s);
	} else if (beresp.status == 302){
		set beresp.ttl = 1h;
	} else if (beresp.status == 404){
		set beresp.ttl = 1m;
	} else {
        set beresp.ttl = 1m;
    }

    if (req.http.host ~ ".dev$" || req.http.host ~ "127.0.0.1"){
        set beresp.ttl = 0s;
        set beresp.http.X-Development = 1;
    }
}

sub vcl_deliver {
	if (obj.hits > 0) {
		set resp.http.X-Cache = "HIT";
	} else {
		set resp.http.X-Cache = "MISS";
	}

	remove resp.http.X-Cache-TTL;
	remove resp.http.X-Cache-Vary;
	remove resp.http.X-Cache;
	remove resp.http.Via;
	remove resp.http.Server;
	remove resp.http.X-Varnish;
}

sub vcl_error {
    # Redirect non-https to https
    if (obj.status == 750) {
        set obj.http.Location = obj.response;
        set obj.status = 302;
        return(deliver);
    }
}