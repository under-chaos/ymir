import random
from typing import Dict

import fastapi
import pytest
from fastapi.testclient import TestClient

from app.api.api_v1.api import datasets as m
from app.config import settings
from tests.utils.utils import random_lower_string, random_url


@pytest.fixture(scope="function", autouse=True)
def patch_prepare_dataset(mocker, tmp_path):
    annotations_dir = tmp_path / "anno"
    annotations_dir.mkdir()
    images_dir = tmp_path / "img"
    images_dir.mkdir()
    mocker.patch.object(
        m, "prepare_dataset", return_value={"annotations": str(annotations_dir), "images": str(images_dir)}
    )


@pytest.fixture(scope="function", autouse=True)
def patch_background_task(mocker):
    mocker.patch.object(fastapi, "BackgroundTasks", return_value=mocker.Mock())


@pytest.fixture(scope="function")
def mock_controller(mocker):
    return mocker.Mock()


@pytest.fixture(scope="function")
def mock_db(mocker):
    return mocker.Mock()


@pytest.fixture(scope="function")
def mock_graph_db(mocker):
    return mocker.Mock()


@pytest.fixture(scope="function")
def mock_viz(mocker):
    return mocker.Mock()


def create_dataset(client, headers):
    j = {
        "name": random_lower_string(),
        "input_url": random_url(),
        "strategy": 1,
    }
    r = client.post(f"{settings.API_V1_STR}/datasets/", headers=headers, json=j)
    return r


class TestListDatasets:
    def test_list_datasets_having_results(
        self, client: TestClient, normal_user_token_headers: Dict[str, str], mocker
    ):
        for _ in range(3):
            r = create_dataset(client, normal_user_token_headers)
        r = client.get(
            f"{settings.API_V1_STR}/datasets/", headers=normal_user_token_headers
        )
        datasets = r.json()["result"]["items"]
        total = r.json()["result"]["total"]
        assert "task_progress" in datasets[0]
        assert "progress" in datasets[0]
        assert len(datasets) == total != 0

    def test_list_datasets_not_found(
        self, client: TestClient, normal_user_token_headers
    ):
        r = client.get(
            f"{settings.API_V1_STR}/datasets/",
            headers=normal_user_token_headers,
            params={"ids": "100,200,300"},
        )
        assert r.status_code == 404

    def test_list_datasets_given_ids(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        r = client.get(
            f"{settings.API_V1_STR}/datasets/",
            headers=normal_user_token_headers,
            params={"ids": "1,200,300"},
        )
        datasets = r.json()["result"]["items"]
        total = r.json()["result"]["total"]
        assert total == 1


class TestCreateDataset:
    def test_create_dataset_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        j = {
            "name": random_lower_string(),
            "input_url": random_url(),
            "strategy": 1,
        }
        r = client.post(
            f"{settings.API_V1_STR}/datasets/",
            headers=normal_user_token_headers,
            json=j,
        )
        assert r.json()["code"] == 0


class TestDeleteDatasets:
    def test_delete_dataset_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        assert not r.json()["result"]["is_deleted"]

        r = client.delete(
            f"{settings.API_V1_STR}/datasets/{dataset_id}",
            headers=normal_user_token_headers,
        )
        assert r.json()["result"]["is_deleted"]

    def test_delete_dataset_not_found(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = client.delete(
            f"{settings.API_V1_STR}/datasets/20000", headers=normal_user_token_headers
        )
        assert r.status_code == 404


class TestPatchDatasets:
    def test_update_dataset_name_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        dataset_name = r.json()["result"]["name"]

        new_name = random_lower_string(5)

        r = client.patch(
            f"{settings.API_V1_STR}/datasets/{dataset_id}",
            headers=normal_user_token_headers,
            json={"name": new_name},
        )
        assert r.json()["result"]["name"] == new_name != dataset_name

    def test_update_dataset_name_not_found(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = client.patch(
            f"{settings.API_V1_STR}/datasets/23333333",
            headers=normal_user_token_headers,
            json={"name": "x"},
        )
        assert r.status_code == 404


class TestGetDataset:
    def test_get_dataset_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        r = client.get(
            f"{settings.API_V1_STR}/datasets/{dataset_id}",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        assert r.json()["code"] == 0
        dataset_res = r.json()["result"]
        assert "task_progress" in dataset_res
        assert "progress" in dataset_res
        assert "config" in dataset_res


class TestGetAssets:
    def test_get_assets_of_dataset_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        r = client.get(
            f"{settings.API_V1_STR}/datasets/{dataset_id}/assets",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        assert r.json()["code"] == 0

    def test_get_assets_of_dataset_not_found(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = client.get(
            f"{settings.API_V1_STR}/datasets/23333333/assets",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 404


class TestGetAsset:
    def test_get_asset_by_asset_hash_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = client.get(
            f"{settings.API_V1_STR}/datasets/23333333/assets/abc",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 404

    def test_get_asset_by_asset_hash_not_found(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        r = client.get(
            f"{settings.API_V1_STR}/datasets/{dataset_id}/assets/abc",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        assert r.json()["code"] == 0


class TestGetRandomAsset:
    def test_get_random_asset_succeed(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        mocker.patch.object(m, "get_random_asset_offset", return_value=1)
        r = create_dataset(client, normal_user_token_headers)
        dataset_id = r.json()["result"]["id"]
        r = client.get(
            f"{settings.API_V1_STR}/datasets/{dataset_id}/assets/random",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 200
        assert r.json()["code"] == 0

    def test_get_random_asset_not_found(
        self, client: TestClient, normal_user_token_headers, mocker
    ):
        r = client.get(
            f"{settings.API_V1_STR}/datasets/23333/assets/random",
            headers=normal_user_token_headers,
        )
        assert r.status_code == 404
        assert r.json()["code"] == 4001

    def test_get_random_offset(self, mocker):
        limit = random.randint(100, 200)
        dataset = mocker.Mock(asset_count=limit)
        assert 0 <= m.get_random_asset_offset(dataset) <= limit
