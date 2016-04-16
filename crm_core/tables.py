from cartridge.shop.models import Product, Category
import django_tables2 as tables
from crm_core.custom.custom_columns import (LabelColumn, ButtonsColumn,
                                            ModelDetailLinkColumn,
                                            IncludeColumn,
                                            SafeFieldColumn, CssFieldColumn)
from crm_core.models import (Contract, Customer, Supplier, TaxRate,
                             CustomerBillingCycle, Unit, CustomerGroup)
from django.utils.translation import ugettext_lazy as _


class ContractTable(tables.Table):
    state = LabelColumn(verbose_name=_('Status'))
    name = ModelDetailLinkColumn(verbose_name=_('Name'))
    default_customer = tables.TemplateColumn(
        "<a href='{{ record.default_customer.get_absolute_url }}'>"
        "{{ record.default_customer.short_name }}</a>",
        accessor='default_customer.name', verbose_name=_('Customer'))
    description = tables.Column()
    price = tables.TemplateColumn("{{ record.get_price }}",
                                  accessor='get_price',
                                  verbose_name=_('Price'))
    lastmodification = tables.DateTimeColumn()

    quote = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_quote_detail_url }}'",
                "condition": "record.has_quotes",
            },
            {
                "extra_class": 'btn-primary',
                "gl_icon": 'pencil',
                "onclick": "location.href='{{ record.get_quote_edit_url }}'",
                "condition": "record.has_quotes",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False,
        verbose_name=_('Quote')
    )
    purchase_order = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_purchaseorder_detail_url }}'",
                "condition": "record.has_purchaseorders",
            },
            {
                "extra_class": "btn-success",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_purchaseorder_edit_url }}'",
                "condition": "record.has_purchaseorders",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False,
        verbose_name=_('Purchase Order')
    )
    invoice = ButtonsColumn(
        [
            {
                "extra_class": "btn-default",
                "gl_icon": "search",
                "onclick": "location.href='{{ record.get_invoice_detail_url }}'",
                "condition": "record.has_invoices",
            },
            {
                "extra_class": "btn-warning",
                "gl_icon": "pencil",
                "onclick": "location.href='{{ record.get_invoice_edit_url }}'",
                "condition": "record.has_invoices",
            }
        ],
        attrs={"th": {"width": "90px"}},
        orderable=False,
        verbose_name=_('Invoice')
    )
    edit_status = IncludeColumn(
        'crm_core/includes/contract_row_actions_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )
    edit_contract = IncludeColumn(
        'crm_core/includes/contract_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Contract
        exclude = ('id', 'staff', 'default_supplier', 'default_currency',
                   'dateofcreation', 'lastmodifiedby', 'contact_ptr',
                   'keywords_string', 'gen_description', 'site', 'updated',
                   'created', 'publish_date', 'expiry_date', 'short_url',
                   'in_sitemap', '_meta_title', 'title', 'status', 'slug')
        sequence = ('state', 'name', 'default_customer', 'description',
                    'price', 'lastmodification')
        order_by = ('-lastmodification', 'state')


class CustomerTable(tables.Table):
    name_prefix = tables.TemplateColumn("""{{ record.get_prefix }}""",
                                        accessor='-prefix',
                                        verbose_name=_('Prefix'))
    new_contract = IncludeColumn(
        'crm_core/includes/customer_row_actions_toolbar.html',
        attrs={"th": {"width": "50px"}},
        verbose_name=" ",
        orderable=False
    )
    edit_customer = IncludeColumn(
        'crm_core/includes/customer_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Customer
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation',
                   'lastmodification', 'lastmodifiedby', 'contact_ptr',
                   'keywords_string', 'description', 'gen_description', 'site',
                   'updated', 'created', 'publish_date', 'expiry_date',
                   'short_url', 'in_sitemap', '_meta_title', 'title', 'status',
                   'slug')
        sequence = ('name_prefix', 'firstname', 'name', 'default_currency')
        order_by = ('name', 'firstname')


class SupplierTable(tables.Table):
    name = ModelDetailLinkColumn(accessor='name')
    edit_supplier = IncludeColumn(
        'crm_core/includes/supplier_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Supplier
        exclude = ('id', 'billingcycle', 'prefix', 'dateofcreation',
                   'lastmodification', 'lastmodifiedby', 'contact_ptr',
                   'keywords_string', 'description', 'gen_description', 'site',
                   'updated', 'created', 'publish_date', 'expiry_date',
                   'short_url', 'in_sitemap', '_meta_title', 'title', 'status',
                   'slug')
        sequence = ('name', 'default_currency')
        order_by = ('name', )


class ProductTable(tables.Table):
    unit = CssFieldColumn('record.item_unit.unit', verbose_name=_('Unit'))
    tax = CssFieldColumn('record.item_tax.tax', verbose_name=_('Taxrate'))
    description = SafeFieldColumn('record.description')
    edit_product = IncludeColumn(
        'crm_core/includes/product_row_edit_toolbar.html',
        attrs={"th": {"width": "120px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Product
        exclude = ('id', 'rating_count', 'rating_sum', 'publish_date',
                   'expiry_date', 'short_url', 'in_sitemap', 'sale_id',
                   'sale_price', 'sale_from', 'sale_to', 'sku', 'content',
                   'image', 'date_added', 'related_products',
                   'upsell_products', 'product_ptr', 'keywords_string', 'site',
                   'slug', 'gen_description', '_meta_title', 'rating_average',
                   'created')
        sequence = ('status', 'title', 'description', 'available',
                    'unit_price', 'num_in_stock', 'unit', 'tax')
        order_by = ('id', )


class TaxTable(tables.Table):
    edit_tax = IncludeColumn(
        'crm_core/includes/tax_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = TaxRate
        exclude = ('id', )


class BillingCycleTable(tables.Table):
    edit_billingcycle = IncludeColumn(
        'crm_core/includes/billingcycle_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerBillingCycle
        exclude = ('id', )


class UnitTable(tables.Table):
    edit_unit = IncludeColumn(
        'crm_core/includes/unit_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Unit
        exclude = ('id', )


class ProductCategoryTable(tables.Table):
    edit_category = IncludeColumn(
        'crm_core/includes/category_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = Category
        exclude = ('id', 'combined', 'in_menus', 'featured_image',
                   'expiry_date', 'in_sitemap', 'description', 'short_url',
                   'publish_date', 'status', 'site', 'slug', 'created',
                   'updated', 'gen_description', 'keywords_string', 'keywords',
                   '_meta_title', 'titles', 'content_model', 'login_required',
                   'parent', '_order', 'content', 'sale', 'price_max',
                   'price_min', 'page_ptr')


class CustomerGroupTable(tables.Table):
    edit_customergroup = IncludeColumn(
        'crm_core/includes/customergroup_row_edit_toolbar.html',
        attrs={"th": {"width": "90px"}},
        verbose_name=" ",
        orderable=False
    )

    class Meta:
        model = CustomerGroup
        exclude = ('id', )
