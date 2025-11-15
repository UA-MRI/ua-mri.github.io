module Jekyll
    class ImageGalleryTag < Liquid::Tag
      def initialize(tag_name, folder_path, tokens)
        super
        @folder_path = folder_path.strip
      end
  
      def render(context)
        site   = context.registers[:site]
        source = site.source
        folder = File.join(source, @folder_path)
  
        return "" unless Dir.exist?(folder)
  
        # Get all image files, excluding Zone.Identifier files
        images = Dir.glob(File.join(folder, "*")).select do |f|
          File.file?(f) &&
            f.match(/\.(jpg|jpeg|png|gif|heic|webp)$/i) &&
            !f.include?("Zone.Identifier")
        end.sort.map { |f| File.basename(f) }
  
        
        return "" if images.empty?
  
        gallery_id = "gallery-#{@folder_path.gsub(/[^a-z0-9]/i, '-')}"
        baseurl    = site.config['baseurl'] || ''
  
        # Root gallery div – now using Spotlight group
        html = %Q(<div class="spotlight-group image-gallery" id="#{gallery_id}">\n)
  
        # Inline CSS to make it a nice responsive grid
        html += %Q(<style>
  ##{gallery_id} {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 15px;
  }
  
  ##{gallery_id} a.spotlight {
    display: block;
    width: 100%;
  }
  
  ##{gallery_id} img {
    display: block;
    width: 100%;
    height: auto;
    object-fit: contain;
    border-radius: 6px;
  }
  </style>\n)
  
        images.each do |image_file|
          image_path = File.join(@folder_path, image_file).gsub(/\\/, '/')
          image_name = File.basename(image_file, File.extname(image_file))
  
          # Build URL: baseurl + / + image_path (Jekyll serves assets from root)
          url_path = baseurl.empty? ? "/#{image_path}" : "#{baseurl}/#{image_path}"
          url_path = url_path.gsub(/\/+/, '/')
  
          html += %Q(  <a class="spotlight" href="#{url_path}">
      <img src="#{url_path}" alt="#{image_name}" />
    </a>\n)
        end
  
        html += "</div>"
        html
      end
    end
  end
  
  Liquid::Template.register_tag('image_gallery', Jekyll::ImageGalleryTag)
  