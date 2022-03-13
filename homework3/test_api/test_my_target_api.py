import ast

import pytest

from api.tools.random_generate import RandomGenerate
from test_api.base_api import BaseApi


class TestApi(BaseApi):

    @pytest.mark.API
    def test_valid_login(self):
        assert self.api_client.session.cookies['z']
        assert self.api_client.session.cookies['mc']
        assert self.api_client.session.cookies['mrcu']
        assert self.api_client.session.cookies['sdc']
        assert self.api_client.session.cookies['csrftoken']

    @pytest.mark.API
    def test_create_campaign(self):
        name = RandomGenerate.generate_random_name()
        response = self.create_campaign(name)

        id_campaign = ast.literal_eval(response.text)['id']

        assert self.check_campaign_is_created(id_campaign, name)

        self.delete_campaign(id_campaign)

        assert self.check_campaign_is_deleted(id_campaign, name)

    @pytest.mark.API
    def test_create_segment(self):
        name = RandomGenerate.generate_random_name()
        response = self.create_segment(name)

        id_segment = ast.literal_eval(response.text)['id']

        assert self.check_segment_is_created(id_segment, name)

        self.delete_segment(id_segment)

        assert self.check_segment_is_deleted(id_segment, name)

    @pytest.mark.API
    def test_delete_segment(self):
        name = RandomGenerate.generate_random_name()

        response = self.create_segment(name)

        id_segment = ast.literal_eval(response.text)['id']

        self.delete_segment(id_segment)

        assert self.check_segment_is_deleted(id_segment, name)
