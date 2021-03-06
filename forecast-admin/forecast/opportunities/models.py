from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from localflavor.us.models import USStateField, PhoneNumberField
from opportunities.validators import validate_NAICS


# Create your models here.
class Office(models.Model):
    organization = models.CharField(max_length=30)
    region = models.CharField(max_length=30)

    def __str__(self):
        return "%s (%s)" % (self.organization, self.region)


# The OSBU Advisor is the Office of Small Business Utilization specialist
# who is responsible for the forecast data... 
class OSBUAdvisor(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=200, blank=True, null=True)
    phone = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return "%s (%s)" % (self.name, self.email)

    class Meta:
        verbose_name = "OSBU Advisor"


class Opportunity(models.Model):
    AWARD_STATUS_CHOICES = (
        ("Awarded", "Awarded"),
        ("Award Pending", "Award Pending"),
        ("Solicitation Issued", "Solicitation Issued"),
        ("Drafting Solicitation", "Drafting Solicitation"),
        ("Solicitation Closed", "Solicitation Closed"),
        ("Planning", "Planning"), ("Cancelled", "Cancelled"),
        ("Evaluation Stage", "Evaluation Stage"),
        ("Option Exercise Pending", "Option Exercise Pending"),
        ("Option Exercised", "Option Exercised"),
      )

    SOCIOECONOMIC_CHOICES = (
        ("Small Business", "Small Business"),
        ("Small Disadvantaged Business (includes Section 8a)",
            "Small Disadvantaged Business (includes Section 8a)"),
        ("Woman-Owned Small Business", "Woman-Owned Small Business"),
        ("HUBZone Small Business", "HUBZone Small Business"),
        ("Service Disabled Veteran-owned Small Business",
            "Service Disabled Veteran-owned Small Business"),
        ("Multiple Small Business Categories",
            "Multiple Small Business Categories"),
        ("Other Than Small", "Other Than Small"), ("AbilityOne", "AbilityOne"),
        ("To Be Determined", "To Be Determined"),
        ("To Be Determined-BPA", "To Be Determined-BPA"),
        ("To Be Determined-IDIQ", "To Be Determined-IDIQ")
    )

    CONTRACT_TYPE_CHOICES = (
        ("Fixed Price with Economic Price Adjustment",
            "Fixed Price with Economic Price Adjustment"),
        ("Fixed Price Incentive", "Fixed Price Incentive"),
        ("Fixed Price Award Fee", "Fixed Price Award Fee"),
        ("Cost Plus Award Fee", "Cost Plus Award Fee"),
        ("Cost No Fee", "Cost No Fee"),
        ("Cost Sharing", "Cost Sharing"),
        ("Cost Plus Fixed Fee", "Cost Plus Fixed Fee"),
        ("Cost Plus Incentive Fee", "Cost Plus Incentive Fee"),
        ("Time and Materials", "Time and Materials"),
        ("Labor Hours", "Labor Hours"),
        ("Order Dependent", "Order Dependent"),
        ("To Be Determined", "To Be Determined"),
        ("Interagency Agreement", "Interagency Agreement")
    )

    PROCUREMENT_METHOD_CHOICES = (
        ("GSA Schedule", "GSA Schedule"),
        ("Government-wide Agency Contract-GWAC",
            "Government-wide Agency Contract-GWAC"),
        ("Basic Ordering Agreement", "Basic Ordering Agreement"),
        ("Blanket Purchase Agreement-BPA", "Blanket Purchase Agreement-BPA"),
        ("Multi-Agency Contract", "Multi-Agency Contract"),
        ("BPA Call", "BPA Call"),
        ("Purchase Order", "Purchase Order"),
        ("Definitive Contract", "Definitive Contract"),
        ("Ability One", "Ability One"),
        ("Indefinite Delivery Indefinite Quantity-IDIQ",
            "Indefinite Delivery Indefinite Quantity-IDIQ"),
        ("Negotiated", "Negotiated"),
        ("Sealed Bid", "Sealed Bid"),
        ("Contract", "Contract"),
        ("Commercial Item Contract", "Commercial Item Contract"),
        ("GSA Schedules Program BPA", "GSA Schedules Program BPA"),
        ("Indefinite Delivery Vehicle (IDV)",
            "Indefinite Delivery Vehicle (IDV)"),
        ("Purchase Order", "Purchase Order"),
        ("Order under IDV", "Order under IDV"),
        ("Order under GSA Schedules Program",
            "Order under GSA Schedules Program"),
        ("Order under GSA Schedules Program BPA",
            "Order under GSA Schedules Program BPA"),
        ("To Be Determined", "To Be Determined"),
        ("Definitive Contract other than IDV",
            "Definitive Contract other than IDV"),
        ("Indefinite Delivery Vehicle Base Contract",
            "Indefinite Delivery Vehicle Base Contract"),
        ("Order under GSA Federal Supply Schedules Program",
            "Order under GSA Federal Supply Schedules Program"),
        ("Order under IDV", "Order under IDV"),
        ("Purchase Order", "Purchase Order"),
        ("Contract modification", "Contract modification"),
        ("Ability One", "Ability One"),
        ("Call Order under GSA Schedules BPA",
            "Call Order under GSA Schedules BPA"),
        ("To Be Determined", "To Be Determined"),
        ("GSA Schedule Contract", "GSA Schedule Contract"),
        ("Negotiated", "Negotiated"),
        ("Sealed Bid", "Sealed Bid"),
        ("Government-wide Agency Contract-GWAC",
            "Government-wide Agency Contract-GWAC"),
        ("Commercial Item Contract", "Commercial Item Contract"),
        ("GSA Schedules Program BPA", "GSA Schedules Program BPA"),
        ("BPA Call", "BPA Call"),
        ("Basic Ordering Agreement", "Basic Ordering Agreement"),
        ("Blanket Purchase Agreement-BPA", "Blanket Purchase Agreement-BPA"),
        ("Multi-Agency Contract", "Multi-Agency Contract")
      )

    COMPETITION_CHOICES = (
        ("Sole Source", "Sole Source"),
        ("Full and Open", "Full and Open"),
        ("Set-Aside", "Set-Aside"),
        ("Partial Small Business Set-Aside",
            "Partial Small Business Set-Aside"),
        ("A/E Procedures", "A/E Procedures"),
        ("Full and Open Competition", "Full and Open Competition"),
        ("Not Available for Competition (e.g., 8a sole source, HUBZone & \
            SDVOSB sole source, Ability One, all > SAT)",
            "Not Available for Competition (e.g., 8a sole source, HUBZone & \
            SDVOSB sole source, Ability One, all > SAT)"),
        ("Not Competed (e.g., sole source, urgency, etc., all > SAT)",
            "Not Competed (e.g., sole source, urgency, etc., all > SAT)"),
        ("Full and Open after exclusion of sources (competitive small \
            business set-asides, competitive 8a)",
            "Full and Open after exclusion of sources (competitive small \
            business set-asides, competitive 8a)"),
        ("Follow On to Competed Action", "Follow On to Competed Action"),
        ("Competed under SAP", "Competed under SAP"),
        ("Not Competed under SAP (e.g., Urgent, Sole source, Logical \
            Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)",
            "Not Competed under SAP (e.g., Urgent, Sole source, Logical \
            Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)"),
        ("Competitive Delivery Order Fair Opportunity Provided",
            "Competitive Delivery Order Fair Opportunity Provided"),
        ("Non-Competitive Delivery Order", "Non-Competitive Delivery Order"),
        ("Fair Opportunity", "Fair Opportunity"),
        ("Sole-Source", "Sole-Source"),
        ("Limited Sources", "Limited Sources"),
        ("To Be Determined", "To Be Determined"),
        ("Competitive Schedule Buy", "Competitive Schedule Buy"),
        ("Full and Open after exclusion of sources (competitive small business \
            set-asides, competitive 8a)",
            "Full and Open after exclusion of sources (competitive small \
            business set-asides, competitive 8a)"),
        ("Full and Open Competition Unrestricted",
            "Full and Open Competition Unrestricted"),
        ("Not Available for Competition (e.g., 8a sole source, HUBZone & \
            SDVOSB sole source, Ability One, all > SAT)",
            "Not Available for Competition (e.g., 8a sole source, HUBZone & \
            SDVOSB sole source, Ability One, all > SAT)"),
        ("Not Competed (e.g., sole source, urgency, etc., all > SAT)",
            "Not Competed (e.g., sole source, urgency, etc., all > SAT)"),
        ("Not Competed under SAP (e.g., Urgent, Sole source, Logical \
            Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)",
            "Not Competed under SAP (e.g., Urgent, Sole source, Logical \
            Follow-On, 8a, HUBZone & SDVOSB sole source, all < SAT)"),
        ("A/E Procedures", "A/E Procedures"),
        ("Competed under SAP", "Competed under SAP"),
        ("Follow On to Competed Action (FAR 6.302-1)",
            "Follow On to Competed Action (FAR 6.302-1)"),
        ("Competitive Delivery Order - Fair Opportunity Provided",
            "Competitive Delivery Order - Fair Opportunity Provided"),
        ("Non-Competitive Delivery Order", "Non-Competitive Delivery Order"),
        ("To Be Determined", "To Be Determined"),
        ("Limited Sources FSS Order", "Limited Sources FSS Order"),
        ("Competitive Schedule Buy", "Competitive Schedule Buy"),
        ("Partial Small Business Set-Aside",
            "Partial Small Business Set-Aside")
     )

    NEW_REQUIREMENT_CHOICES = (
        ("New Requirement", "New Requirement"),
        ("Option", "Option"),
        ("To Be Determined", "To Be Determined"),
        ("Recompete", "Recompete")
    )

    FUNDING_AGENCY_CHOICES = (
        ("GSA funded", "GSA funded"),
        ("GSA funded-PBS", "GSA funded-PBS"),
        ("GSA funded-FAS", "GSA funded-FAS"),
        ("GSA funded-IAD", "GSA funded-IAD"),
        ("GSA funded-Other", "GSA funded-Other"),
        ("Non-GSA funded", "Non-GSA funded"),
        ("Both", "Both"),
        ("To Be Determined", "To Be Determined")
    )

    office = models.ForeignKey(Office, blank=True, null=True)
    award_status = models.CharField(max_length=50, default="Planning",
                                    choices=AWARD_STATUS_CHOICES)
    description = models.CharField("Product or Service Description",
                                   max_length=200)
    place_of_performance_city = models.CharField(max_length=100,
                                                 default="Washington")
    place_of_performance_state = USStateField(default="DC")
    naics = models.CharField("Primary NAICS Code",
                             max_length=5, blank=True, null=True,
                             validators=[validate_NAICS])
    socioeconomic = models.CharField("Socioeconomic Category", max_length=50,
                                     choices=SOCIOECONOMIC_CHOICES,
                                     default="To Be Determined")
    procurement_method = models.CharField("Procurement Method", max_length=200,
                                          choices=PROCUREMENT_METHOD_CHOICES,
                                          default="To Be Determined")
    contract_type = models.CharField("Contract Type", max_length=200,
                                     choices=CONTRACT_TYPE_CHOICES,
                                     default="To Be Determined")
    competition_strategy = models.CharField(max_length=200,
                                            choices=COMPETITION_CHOICES,
                                            default="To Be Determined")
    price_min = models.DecimalField(max_length=200, decimal_places=2,
                                    max_digits=16, blank=True, null=True)
    price_max = models.DecimalField(max_length=200, decimal_places=2,
                                    max_digits=16, blank=True, null=True)
    delivery_order_value = models.CharField(max_length=200,
                                            blank=True, null=True)
    incumbent_name = models.CharField("Incumbent Contractor Name",
                                      max_length=200, blank=True, null=True)
    new_requirement = models.CharField(max_length=200,
                                       choices=NEW_REQUIREMENT_CHOICES,
                                       default="To Be Determined")
    funding_agency = models.CharField(max_length=200,
                                      choices=FUNDING_AGENCY_CHOICES,
                                      default="To Be Determined")
    estimated_solicitation_date = models.DateField(blank=True, null=True)
    fedbizopps_link = models.CharField(max_length=200, blank=True, null=True)
    # TODO: going to make these choices...
    estimated_fiscal_year = models.IntegerField(default=2016)
    estimated_fiscal_year_quarter = models.IntegerField(
        default=1, validators=[MaxValueValidator(4)]
    )
    # Note: This can probably get split out into another model
    point_of_contact_name = models.CharField(max_length=200,
                                             blank=True, null=True)
    point_of_contact_email = models.EmailField(max_length=200,
                                               blank=True, null=True)
    point_of_contact_phone = PhoneNumberField(blank=True, null=True)
    osbu_advisor = models.ForeignKey(OSBUAdvisor, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return "%s (%s)" % (self.description, self.estimated_fiscal_year)

    class Meta:
        verbose_name_plural = "Opportunities"
