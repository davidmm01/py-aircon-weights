from exceptions import APICallFailure

import requests

from constants import (CONVERSION_FACTOR, ENDPOINT_SLUG, INITIAL_QUERY,
                       TARGET_CATEGORY)


def get_product_dimensions():
    """Retrieve the product dimensions from the downstream API.

    As this code is being tailored to handle very large data sets, note that the function
    discards all product information that is not essential, i.e. product names, weights,
    and labels of the dimensions.  Ideally the downstream call should be in a separate
    function, but grouping it with the logic to strip unnecessary data is pivotal when
    dealing with large data sets.
    """

    product_dimensions = []

    next_query = INITIAL_QUERY

    while next_query is not None:
        response = requests.get(ENDPOINT_SLUG + next_query)

        if response.status_code != 200:
            raise APICallFailure

        response_json = response.json()

        for item in response_json["objects"]:
            if item["category"] == TARGET_CATEGORY:
                dims = item["size"]
                # explicitly grab dimensions by name to ensure integrity/fail early on bad data
                product_dimensions.append([dims["width"], dims["length"], dims["height"]])

        next_query = response_json["next"]

    return product_dimensions


def calculate_cubic_weight(width, length, height):
    """Calculates the cubic weight of a product.

    Args:
        width: width of product (in cm)
        length: length of product (in cm)
        height: height of product (in cm)

    Returns:
        int or float
    """

    # convert width, length and height from centimetres to metres
    width /= 100
    length /= 100
    height /= 100

    return width*length*height*CONVERSION_FACTOR


def calculate_average_cubic_weight(product_dimensions):
    """Coordinates the calculation of product weights and then calculates the average.

    Args:
        product_dimensions: an array representation of product dimensions.  As per
                            get_product_dimensions, each element of the array should be an array
                            containing three elements, being the width, length and height

    Returns:
        int or float
    """
    if len(product_dimensions) == 0:
        return 0

    cubic_weight_total = 0
    for dimensions in product_dimensions:
        cubic_weight_total += calculate_cubic_weight(dimensions[0], dimensions[1], dimensions[2])
    return cubic_weight_total/len(product_dimensions)


def main():
    try:
        dimensions = get_product_dimensions()
    except APICallFailure:
        print("Failed to retrieve product data from the API, exiting...")
        return

    average = calculate_average_cubic_weight(dimensions)
    print(f"Average cubic weight of products in {TARGET_CATEGORY} is: {round(average,2)}kg")


if __name__ == "__main__":  # pragma: no cover
    main()
