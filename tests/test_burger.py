from unittest.mock import Mock
import pytest
from praktikum.burger import Burger


class Bun:

    def get_name(self):
        pass

    def get_price(self):
        pass


class Ingredient:

    def get_name(self):
        pass

    def get_price(self):
        pass

    def get_type(self):
        pass


class TestBurger:

    def test_init_burger_is_empty(self):
        burger = Burger()
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns_adds_bun(self):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        burger.set_buns(mock_bun)
        assert burger.bun == mock_bun

    def test_add_ingredient_adds_to_list(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        assert burger.ingredients == [mock_ingredient]

    def test_remove_ingredient_clears_list(self):
        burger = Burger()
        mock_ingredient = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ingredient)
        burger.remove_ingredient(0)
        assert burger.ingredients == []

    def test_move_ingredient_swaps_positions(self):
        burger = Burger()
        mock_ing1 = Mock(spec=Ingredient)
        mock_ing2 = Mock(spec=Ingredient)
        burger.add_ingredient(mock_ing1)
        burger.add_ingredient(mock_ing2)
        burger.move_ingredient(0, 1)
        assert burger.ingredients == [mock_ing2, mock_ing1]

    @pytest.mark.parametrize(
        "bun_price, ingredient_price, expected_total",
        [
            (100.0, 50.0, 250.0),
            (0.0, 10.0, 10.0),
            (250.5, 0.0, 501.0),
            (150.0, 100.0, 400.0),
        ],
    )
    def test_get_price_calculation(
        self, bun_price, ingredient_price, expected_total
    ):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_price.return_value = bun_price
        burger.set_buns(mock_bun)

        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_price.return_value = ingredient_price
        burger.add_ingredient(mock_ingredient)
        assert burger.get_price() == expected_total

    @pytest.mark.parametrize(
        "bun_name, ing_type, ing_name, ing_price, expected_price_str",
        [
            ("Краторная булка", "SAUCE", "чили", 50.0, "Price: 250.0"),
            ("Супер булка", "FILLING", "биг котлета", 150.0, "Price: 350.0"),
        ],
    )
    def test_get_receipt_formatting(
        self, bun_name, ing_type, ing_name, ing_price, expected_price_str
    ):
        burger = Burger()
        mock_bun = Mock(spec=Bun)
        mock_bun.get_name.return_value = bun_name
        mock_bun.get_price.return_value = 100.0
        burger.set_buns(mock_bun)

        mock_ingredient = Mock(spec=Ingredient)
        mock_ingredient.get_type.return_value = ing_type
        mock_ingredient.get_name.return_value = ing_name
        mock_ingredient.get_price.return_value = ing_price
        burger.add_ingredient(mock_ingredient)

        receipt = burger.get_receipt()
        assert f"(==== {bun_name} ====)" in receipt
        assert f"= {ing_type.lower()} {ing_name} =" in receipt
        assert expected_price_str in receipt
