{% load i18n %}<div id="tumblelog">
    {% for post in posts %}
        {% include post.template %}
    {% endfor %}
    <div class="pagination">
        {% if page_obj.has_previous %}
            <a href="?page={{ page_obj.previous_page_number }}">« previous</a>
        {% endif %}

        <span class="current">
            {% blocktrans with cur_page=page_obj.number num_pages=paginator.num_pages %}
                Page {{ cur_page }} of {{ num_pages }}
            {% endblocktrans %}
        </span>

        {% if page_obj.has_next %}
            <a href="?page={{ page_obj.next_page_number }}">next »</a>
        {% endif %}
    </div>
</div>

