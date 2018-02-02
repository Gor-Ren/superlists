from django.test import TestCase
from lists.models import Item


class ItemModelTest(TestCase):

    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = 'The first list item'
        first_item.save()

        second_item = Item()
        second_item.text = 'Item the second'
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(2, saved_items.count())

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first list item')
        self.assertEqual(second_saved_item.text, 'Item the second')


class HomePageTest(TestCase):

    def test_only_saves_items_when_necessary(self):
        self.client.get('/')
        self.assertEqual(0, Item.objects.count())

    def test_home_page_returns_correct_html(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        self.client.post('/', data={'item_text': 'A new list item'})

        # check item has been saved to DB
        self.assertEqual(1, Item.objects.count())
        new_item = Item.objects.first()
        self.assertEqual('A new list item', new_item.text)

    def test_redirects_after_POST(self):
        response = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertEqual(302, response.status_code)
        self.assertEqual('/lists/the-only-list-in-the-world',
                         response['location'])


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_all_list_items(self):
        Item.objects.create(text='first')
        Item.objects.create(text='second')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'first')
        self.assertContains(response, 'second')
