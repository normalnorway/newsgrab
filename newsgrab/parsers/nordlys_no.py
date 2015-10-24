""" Nordlys.no

Note: Looks like running same system as ba.no (Bergensavisen)

<meta property="article:published_time" content="2015-09-03T17:56:14.000Z" />
<meta property="article:modified_time" content="2015-09-03T20:39:18.000+0200" />

<time datetime="2015-09-03T17:56:14.000Z" itemprop="datePublished">03. september 2015, kl. 19:56</time>
<time datetime="2015-09-03T20:39:18.000+0200" itemprop="dateModified">03. september 2015, kl. 20:39</time>

<link rel="canonical" href="..." />

COUNT   ITEMPROP
  1     articleBody
  1     associatedMedia
  2     author
  1     caption
  1     contentURL
  1     dateModified
  1     datePublished
  1     headline
  2     keywords
  1     name

# Interesting stuff
<ul itemprop="keywords">
  <li><a href="/hasj">hasj</a></li>
  <li><a href="/narkotika">narkotika</a></li>
</ul>

<a href="mailto:..." itemscope="" itemprop="author" itemtype="http://schema.org/Person">
    <span itemprop="name">Some Name</span>
</a>

<div itemprop="associatedMedia">
  <figure itemscope="itemscope" itemtype="http://schema.org/ImageObject">
    <picture>
      <source srcset="http://g.api.no/obscura/API/dynamic/r1/ece5/tr_980_665_l_f/0000/noly/2015/9/3/16/anita.jpg?chk=D68CF1" media="(min-width:769px)" />
      <source srcset="http://g.api.no/obscura/API/dynamic/r1/ece5/tr_768_521_l_f/0000/noly/2015/9/3/16/anita.jpg?chk=E6FD5A" media="(min-width:481px)" />
      <source srcset="http://g.api.no/obscura/API/dynamic/r1/ece5/tr_480_326_l_f/0000/noly/2015/9/3/16/anita.jpg?chk=5A60B1" media="(max-width:480px)" />
      <img src="http://g.api.no/obscura/API/dynamic/r1/ece5/tr_630_428_l_f/0000/noly/2015/9/3/16/anita.jpg?chk=AF35A0" alt="Anita  Hermandsen, leder i U18-gruppen i Troms politidistrikt. Foto: Yngve Olsen Saebbe"
        itemprop="contentURL" />
    </picture>
    <figcaption itemprop="caption">...</figcaption>
  </figure>
</div>
"""

from . import OpenGraphParser

class Parser (OpenGraphParser):
    use_canonical_url = True
