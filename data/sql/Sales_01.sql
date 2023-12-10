SELECT pc.Name AS CategoryName,
    p.name AS ProductName
FROM [SalesLT].[ProductCategory] pc
INNER JOIN [SalesLT].[Product] p
    ON pc.ProductCategoryId = p.ProductCategoryId;