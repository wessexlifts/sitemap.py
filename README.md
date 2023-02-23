# sitemap.py

A standalone Python 3 script to generate XML sitemaps. Mainly used for the Wessex website, but adapted for use by other URLs, etc.

Only tested with Windows 10.

## Method

It uses some pretty simple but effective methodology:

**Priority:**

Determined by page depth and giving slightly more priority to `index` files.

**robots.txt:**

Does a quick search of the `robots.txt` file (if one exists) to see if there are any pages that need to be ignored.

**Other:**

Other features are simple, such as `<loc>` just being the location of the file and `<lastmod>` jut being the last modified time.

Example output is:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<!-- Generated with https://github.com/wessexlifts/sitemap.py -->
<url>
    <loc>https://wessexlifts.co.uk/about-wessex</loc>
    <lastmod>2022-02-24T10:35:49+00:00</lastmod>
    <priority>0.75</priority>
</url>
<url>
    <loc>https://wessexlifts.co.uk/blog/2014/flood</loc>
    <lastmod>2022-09-15T11:00:26+00:00</lastmod>
    <priority>0.30</priority>
</url>
<url>
    <loc>https://wessexlifts.co.uk/</loc>
    <lastmod>2022-11-10T12:03:39+00:00</lastmod>
    <priority>1.00</priority>
</url>
<!--...-->
</urlset>
```

## Usage

*TODO:* This section is under development. At the moment, the script is only configured to work with only Wessex Lifts site settings (PHP files, no way to input new URL without editing the Python script directly), but when more features are added, this will be updated.

## Contributing

We're not currently looking for public contributions at this time. If you find anything that needs changing, please [contact us](mailto:marketing@wessexlifts.co.uk) or submit and [issue](https://github.com/wessexlifts/sitemap.py/issues).

## License

Under the MIT Public License. See [License](/LICENSE) file for more information.
