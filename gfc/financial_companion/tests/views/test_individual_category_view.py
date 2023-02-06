from .test_view_base import ViewTestCase
from financial_companion.models import User, Category, CategoryTarget, Transaction
from django.http import HttpResponse
from django.urls import reverse
from django.db.models import Q


class IndividualCategoryViewTestCase(ViewTestCase):
    """Unit tests of the individual category view"""

    def setUp(self):
        self.user: User = User.objects.get(username="@johndoe")
        self.category: Category = Category.objects.filter(user=self.user)[0]
        self.url: str = reverse("individual_category", kwargs={"pk": self.category.id, "filter_type": "all"})

    def test_valid_individual_category_url(self):
        self.assertEqual(self.url, f"/individual_category/{self.category.id}/all/")

    def test_valid_get_view_individual_category(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_category.html")
        category: Category = response.context["category"]
        self.assertTrue(isinstance(category, Category))
        category_targets: Category = response.context["category_targets"]
        for target in category_targets:
            self.assertTrue(isinstance(target, CategoryTarget))
        transactions: list[Transaction] = response.context["transactions"]
        for transaction in transactions:
            self.assertTrue(isinstance(transaction, Transaction))
    
    # TODO: test for filter types (do once can get transactions from user model)
    
    def test_valid_category_belongs_to_user(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_category.html")
    
    def test_invalid_category_does_not_belong_to_user(self):
        self._login(self.user)
        category: Category = Category.objects.filter(~Q(user=self.user))[0]
        url: str = reverse("individual_category", kwargs={"pk": category.id, "filter_type": "all"})
        response: HttpResponse = self.client.get(url, follow=True)
        response_url: str = reverse("dashboard")
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, "pages/dashboard.html")

    def test_valid_category_has_targets(self):
        self._login(self.user)
        response: HttpResponse = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_category.html")
        category_targets: Category = response.context["category_targets"]
        for target in category_targets:
            self.assertTrue(isinstance(target, CategoryTarget))
        self.assertGreater(len(category_targets), 0)
    
    def test_valid_category_does_not_have_targets(self):
        self._login(self.user)
        category: Category = Category.objects.filter(user=self.user)[2]
        url: str = reverse("individual_category", kwargs={"pk": category.id, "filter_type": "all"})
        response: HttpResponse = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/individual_category.html")
        category_targets: Category = response.context["category_targets"]
        self.assertEqual(len(category_targets), 0)

    def test_invalid_get_view_redirects_when_not_logged_in(self):
        self._assert_require_login(self.url)